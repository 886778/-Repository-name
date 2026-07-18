import { expect, test } from '@playwright/test';

test('shows the M0 bootstrap page', async ({ page }) => {
  await page.goto('/');
  await expect(
    page.getByRole('heading', { name: 'AI 八字命理分析平台' }),
  ).toBeVisible();
  await expect(page.getByText('M0 工程骨架已就绪')).toBeVisible();
});
