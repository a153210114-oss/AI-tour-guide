(function (root, factory) {
  const api = factory();
  if (typeof module === "object" && module.exports) module.exports = api;
  if (root) root.LiveTranslation = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  async function connect({ targetLocale, visitorId, audioElement, onTranscript, onState }) {
    onState?.("connecting");
    const secretResponse = await fetch("/api/translation/client-secret", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_locale: targetLocale, visitor_id: visitorId }),
    });
    const secret = await secretResponse.json();
    if (!secretResponse.ok) throw new Error(secret.error || "Translation session could not start");
    if (!secret.value) throw new Error("Translation provider did not return a client secret");
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    const peer = new RTCPeerConnection();
    peer.addTrack(stream.getAudioTracks()[0], stream);
    peer.ontrack = ({ streams }) => { audioElement.srcObject = streams[0]; };
    const events = peer.createDataChannel("oai-events");
    events.onmessage = ({ data }) => {
      const event = JSON.parse(data);
      if (event.type === "session.output_transcript.delta") onTranscript?.(event.delta);
    };
    const offer = await peer.createOffer();
    await peer.setLocalDescription(offer);
    const answer = await fetch("https://api.openai.com/v1/realtime/translations/calls", {
      method: "POST", headers: { Authorization: `Bearer ${secret.value}`, "Content-Type": "application/sdp" }, body: offer.sdp,
    });
    if (!answer.ok) throw new Error("Realtime translation connection failed");
    await peer.setRemoteDescription({ type: "answer", sdp: await answer.text() });
    onState?.("connected");
    return () => { stream.getTracks().forEach((track) => track.stop()); peer.close(); onState?.("stopped"); };
  }

  return { connect };
});
