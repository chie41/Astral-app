import { Page, expect } from '@playwright/test';

export class TestHelpers {
  constructor(private page: Page) {}

  // Kiểm tra navbar có hiển thị đúng không
  async verifyNavbar() {
    await expect(this.page.locator('.navbar')).toBeVisible();
    await expect(this.page.locator('.logo-text')).toHaveText('Astral');
    await expect(this.page.locator('.nav-links a[href="dashboard.html"]')).toBeVisible();
    await expect(this.page.locator('.user')).toBeVisible();
  }

  // Kiểm tra dropdown user
  async testUserDropdown() {
    const userDropdown = this.page.locator('.user');
    const dropdown = this.page.locator('.dropdown, .user-dropdown');
    
    // Click để mở dropdown
    await userDropdown.click();
    await expect(dropdown).toBeVisible();
    
    // Kiểm tra các menu items
    await expect(this.page.locator('.menu-item')).toHaveCount(5);
    
    // Click outside để đóng dropdown
    await this.page.locator('body').click();
    await expect(dropdown).toBeHidden();
  }

  // Mock localStorage data
  async setupLocalStorage() {
    await this.page.addInitScript(() => {
      localStorage.setItem('projectName', 'Test Project');
      localStorage.setItem('projectDescription', 'Test Description');
      localStorage.setItem('selectedProjectType', 'Image Classification');
      localStorage.setItem('selectedDatasets', JSON.stringify(['1', '2']));
      localStorage.setItem('selectedTargetColumn', 'Product_Name');
      localStorage.setItem('selectedImageColumn', 'url_thumbnail');
      localStorage.setItem('trainingDuration', '2');
      localStorage.setItem('expectedAccuracy', '85');
      localStorage.setItem('selectedPerformLevel', '2');
    });
  }

  // Clear localStorage
  async clearLocalStorage() {
    await this.page.addInitScript(() => {
      localStorage.clear();
    });
  }

  // Kiểm tra responsive design
  async testResponsive() {
    // Test tablet view
    await this.page.setViewportSize({ width: 768, height: 1024 });
    await expect(this.page.locator('.navbar')).toBeVisible();
    
    // Test mobile view
    await this.page.setViewportSize({ width: 375, height: 667 });
    await expect(this.page.locator('.navbar')).toBeVisible();
    
    // Reset to desktop
    await this.page.setViewportSize({ width: 1920, height: 1080 });
  }

  // Mock API responses
  async mockApiResponses() {
    // Mock datasets API
    await this.page.route('**/api/datasets', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            name: 'Test Dataset 1',
            description: 'Test dataset description',
            size: '1.2GB',
            columns: ['col1', 'col2', 'col3'],
            status: 'labeled'
          },
          {
            name: 'Test Dataset 2',
            description: 'Another test dataset',
            size: '2.5GB',
            columns: ['col1', 'col2'],
            status: 'unlabeled'
          }
        ])
      });
    });

    // Mock chat API
    await this.page.route('**/api/chat', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'text/plain',
        body: 'Hello! I can help you create a machine learning project.'
      });
    });
  }

  // Kiểm tra form validation
  async testFormValidation(formSelector: string, requiredFields: string[]) {
    for (const field of requiredFields) {
      const input = this.page.locator(field);
      await input.fill('');
      await input.blur();
      
      // Kiểm tra submit button bị disable
      const submitBtn = this.page.locator(`${formSelector} button[type="submit"], ${formSelector} .next-step-btn, ${formSelector} .create-dataset-btn`);
      await expect(submitBtn).toBeDisabled();
    }
  }

  // Wait for page load
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForLoadState('domcontentloaded');
  }

  // Take screenshot with timestamp
  async takeScreenshot(name: string) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    await this.page.screenshot({ 
      path: `screenshots/${name}-${timestamp}.png`,
      fullPage: true 
    });
  }
} 