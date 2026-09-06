// Production data contract. SQL migrations under .openai/drizzle own the schema.
export type Company = { id: string; name: string; logoObjectKey: string | null; createdAt: string };
export type Guide = { id: string; companyId: string | null; number: string; name: string; mode: "company" | "rideshare"; createdAt: string };
export type TourSession = { id: string; companyId: string | null; guideId: string; routeName: string; productName: string; serviceDate: string; status: string; joinTokenHash: string; createdAt: string };
export type AudioSegment = { id: string; sessionId: string; guideId: string; objectKey: string; startedAt: string; endedAt: string; latitude: number | null; longitude: number | null; placeName: string | null; consentBasis: string };
export type ContentPack = { id: string; ownerCompanyId: string | null; ownerGuideId: string | null; title: string; status: string; createdAt: string };
export type PackGrant = { id: string; packId: string; granteeCompanyId: string | null; granteeGuideId: string | null; permission: string; grantedAt: string; revokedAt: string | null };
