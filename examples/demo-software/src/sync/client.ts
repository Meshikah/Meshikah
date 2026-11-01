// Synthetic example for card DEMO-1. Illustrative only: not built or run.
// Retries transient partner-API failures (timeouts, 502/503/504) up to 3 times with backoff.

const TRANSIENT = new Set([502, 503, 504]);

export async function syncRecord(send: () => Promise<{ status: number }>, maxAttempts = 3): Promise<number> {
  let attempt = 0;
  while (true) {
    attempt += 1;
    const { status } = await send();
    if (status < 400) return attempt;
    if (!TRANSIENT.has(status) || attempt >= maxAttempts) {
      throw new Error(`sync failed with status ${status} after ${attempt} attempt(s)`);
    }
    await new Promise((resolve) => setTimeout(resolve, 100 * 2 ** attempt));
  }
}
