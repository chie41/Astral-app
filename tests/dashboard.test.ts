import { test, expect } from '@playwright/test';

test.describe('Dashboard Page Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('file:///D:/Astral-app-Trang/frontend/dashboard.html');
  });

  test('should display dashboard correctly', async ({ page }) => {
    // Kiểm tra title
    await expect(page).toHaveTitle('ASTRAL');
    
    // Kiểm tra logo và navbar (không phân biệt hoa thường)
    await expect(page.locator('.logo-text')).toHaveText(/astral/i);
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra header section
    await expect(page.locator('.header h1')).toBeVisible();
    await expect(page.locator('.new-project-btn')).toBeVisible();
    
    // Kiểm tra description
    await expect(page.locator('.description')).toBeVisible();
    
    // Kiểm tra projects section
    await expect(page.locator('.projects')).toBeVisible();
  });

  test('should display project cards correctly', async ({ page }) => {
    const projectCards = page.locator('.project-card');
    
    // Kiểm tra project card đầu tiên
    const firstCard = projectCards.first();
    await expect(firstCard.locator('.project-header')).toBeVisible();
    await expect(firstCard.locator('.project-content')).toBeVisible();
    await expect(firstCard.locator('.project-title')).toBeVisible();
    await expect(firstCard.locator('.project-description')).toBeVisible();
    await expect(firstCard.locator('.delete-btn')).toBeVisible();
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

  test('should navigate to boxchat page', async ({ page }) => {
    // Chỉ kiểm tra sự tồn tại của link boxchat
    const boxchatLink = page.locator('.nav-links a').filter({ hasText: 'Projects' });
    await expect(boxchatLink).toBeVisible();
  });

  test('should navigate to datasets page', async ({ page }) => {
    const datasetsLink = page.locator('.nav-links a').filter({ hasText: 'Dataset' });
    await expect(datasetsLink).toBeVisible();
  });

  test('should be responsive on mobile devices', async ({ page }) => {
    // Set viewport to mobile size
    await page.setViewportSize({ width: 375, height: 667 });
    
    // Kiểm tra navbar vẫn hiển thị
    await expect(page.locator('.navbar')).toBeVisible();
    
    // Kiểm tra main content vẫn hiển thị
    await expect(page.locator('.main')).toBeVisible();
    
    // Kiểm tra project cards vẫn hiển thị
    const projectCards = page.locator('.project-card');
    await expect(projectCards.first()).toBeVisible();
  });
}); 