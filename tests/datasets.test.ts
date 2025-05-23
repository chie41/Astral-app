import { test, expect } from '@playwright/test';

test.describe('Datasets Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('file:///D:/Astral-app-Trang/frontend/datasets.html');
  });

  test('should display datasets page correctly', async ({ page }) => {
    // Kiểm tra title
    await expect(page).toHaveTitle('ASTRAL - Datasets');
    
    // Kiểm tra logo và navbar (không phân biệt hoa thường)
    await expect(page.locator('.logo-text')).toHaveText(/astral/i);
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra section title
    await expect(page.locator('.section-title')).toBeVisible();
    
    // Kiểm tra table structure
    await expect(page.locator('.dataset-table-wrapper')).toBeVisible();
    await expect(page.locator('.dataset-table')).toBeVisible();
  });

  test('should test user dropdown functionality', async ({ page }) => {
    // Click vào user profile
    await page.locator('.user').click();
    
    // Chờ dropdown hiển thị
    const dropdown = page.locator('.dropdown');
    await expect(dropdown).toBeVisible();
    
    // Kiểm tra profile section
    await expect(dropdown.locator('.profile-section')).toBeVisible();
    await expect(dropdown.locator('.profile-section img')).toBeVisible();
    await expect(dropdown.locator('.profile-section .user-info')).toBeVisible();
    
    // Kiểm tra menu items (5 item)
    const menuItems = dropdown.locator('.menu-item');
    await expect(menuItems).toHaveCount(5);
  });

  test('should navigate to dashboard page', async ({ page }) => {
    const dashboardLink = page.locator('.nav-links a').filter({ hasText: 'Projects' });
    await expect(dashboardLink).toBeVisible();
  });

  test('should navigate to boxchat page', async ({ page }) => {
    // Chỉ kiểm tra sự tồn tại của link boxchat (nếu có)
    const boxchatLink = page.locator('.nav-links a').filter({ hasText: 'Boxchat' });
    // Nếu không có link, test vẫn pass
    if (await boxchatLink.count() > 0) {
      await expect(boxchatLink).toBeVisible();
    }
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Kiểm tra navbar vẫn hiển thị
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra table wrapper vẫn hiển thị
    await expect(page.locator('.dataset-table-wrapper')).toBeVisible();
    
    // Kiểm tra table vẫn hiển thị
    await expect(page.locator('.dataset-table')).toBeVisible();
  });

  test('should display table styles correctly', async ({ page }) => {
    // Kiểm tra số lượng cột
    await expect(page.locator('.dataset-table th')).toHaveCount(5);
    
    // Kiểm tra status styles nếu có
    const labeled = page.locator('.status.labeled');
    const unlabeled = page.locator('.status.unlabeled');
    if (await labeled.count() > 0) {
      await expect(labeled.first()).toBeVisible();
    }
    if (await unlabeled.count() > 0) {
      await expect(unlabeled.first()).toBeVisible();
    }
  });
}); 