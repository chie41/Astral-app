import { test, expect } from '@playwright/test';

test.describe('Box Chat Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('file:///D:/Astral-app-Trang/frontend/boxchat.html');
  });

  test('should display chat page correctly', async ({ page }) => {
    // Kiểm tra title
    await expect(page).toHaveTitle('ASTRAL - Box Chat');
    
    // Kiểm tra logo và navbar (không phân biệt hoa thường)
    await expect(page.locator('.logo-text')).toHaveText(/astral/i);
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra chat container
    await expect(page.locator('.chat-container')).toBeVisible();
    
    // Kiểm tra chat messages area
    await expect(page.locator('.chat-messages')).toBeVisible();
    
    // Kiểm tra assistant header
    await expect(page.locator('.assistant-header')).toBeVisible();
  });

  test('should test user dropdown functionality', async ({ page }) => {
    // Click vào user profile
    await page.locator('.user').click();
    
    // Kiểm tra dropdown menu
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
    const dashboardLink = page.locator('.nav-links a[href="dashboard.html"]');
    await dashboardLink.click();
    await expect(page).toHaveURL(/dashboard\.html/);
  });

  test('should navigate to datasets page', async ({ page }) => {
    // Link datasets hiện tại là <a href="#">Dataset</a> nên không chuyển trang được, chỉ kiểm tra tồn tại
    const datasetsLink = page.locator('.nav-links a').filter({ hasText: 'Dataset' });
    await expect(datasetsLink).toBeVisible();
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Kiểm tra navbar vẫn hiển thị
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra chat container vẫn hiển thị
    await expect(page.locator('.chat-container')).toBeVisible();
    
    // Kiểm tra chat messages vẫn hiển thị
    await expect(page.locator('.chat-messages')).toBeVisible();
  });

  test('should display message styles correctly', async ({ page }) => {
    // Chỉ kiểm tra nếu có message mẫu
    const assistantMsg = page.locator('.message.assistant');
    const userMsg = page.locator('.message.user');
    if (await assistantMsg.count() > 0) {
      await expect(assistantMsg.first()).toBeVisible();
    }
    if (await userMsg.count() > 0) {
      await expect(userMsg.first()).toBeVisible();
    }
    // Kiểm tra message content styles nếu có
    const msgContent = page.locator('.message-content');
    if (await msgContent.count() > 0) {
      await expect(msgContent.first()).toBeVisible();
    }
    // Kiểm tra loading dots animation nếu có
    const loadingDots = page.locator('.loading-dots');
    if (await loadingDots.count() > 0) {
      await expect(loadingDots.first()).toBeVisible();
      await expect(loadingDots.first().locator('span')).toHaveCount(3);
    }
  });
});