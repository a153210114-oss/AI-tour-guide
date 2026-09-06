const test = require("node:test");
const assert = require("node:assert/strict");
const channel = require("../visitor/live-channel.js");

test("listen-guide starts disconnected in explicit test mode", () => {
  const state = channel.getInitialChannelState();
  assert.equal(state.mode, "test");
  assert.equal(state.connected, false);
  assert.equal(state.provider, null);
});

test("status copy never claims live translation", () => {
  const state = channel.getInitialChannelState();
  assert.match(channel.describeChannel(state, "zh"), /测试模式.*尚未连接/);
  assert.match(channel.describeChannel(state, "en"), /Test mode.*not connected/);
});

