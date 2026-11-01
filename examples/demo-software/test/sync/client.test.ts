// Synthetic example for card DEMO-1. Illustrative only: not run.
import { syncRecord } from "../../src/sync/client";

test("transient failure is retried (acceptance 1)", async () => {
  const replies = [503, 503, 200];
  const attempts = await syncRecord(async () => ({ status: replies.shift()! }));
  expect(attempts).toBe(3);
});

test("permanent failure is not retried (acceptance 2)", async () => {
  await expect(syncRecord(async () => ({ status: 400 }))).rejects.toThrow("after 1 attempt");
});
