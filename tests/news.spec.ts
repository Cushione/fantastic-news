import { test, expect } from '@playwright/test'
import { login } from './member.spec';

const testingUrl = process.env.TESTING_URL!

test.describe('homepage',() => {
  test.beforeEach(async ({ page }) => {
    await page.goto(testingUrl)
  })

  test("should have title, header and footer", async ({page}) => {
    await expect(page).toHaveTitle("Fantastic News")
    await expect(page.getByTestId("brand-name")).toHaveText("Fantastic News")
    await expect(page.getByTestId("register-link")).toBeVisible()
    await expect(page.getByTestId("login-link")).toBeVisible()
    await expect(page.getByTestId("member-username")).toHaveCount(0)
    await expect(page.getByTestId("logout-link")).toHaveCount(0)
    await expect(page.getByTestId("search")).toBeVisible()
    await expect(page.getByTestId("footer")).toBeVisible()
  })

  test("should display latest news", async ({page}) => {
    const latestArticle = page.locator('#latest-article')
    await expect(latestArticle.getByTestId("latest-article-title")).toBeVisible()
    await expect(latestArticle.getByTestId("latest-article-body")).toBeVisible()
    await expect(latestArticle.getByTestId("latest-article-date")).toBeVisible()
  })

  test("should display main news list", async ({page}) => {
    const mainArticles = page.getByTestId(/main-article-\d/)
    // Expect four main articles to be displayed
    await expect(mainArticles).toHaveCount(4)
    // Expect every article to have a title and image
    for (const article of await mainArticles.all()) {
      await expect(article.getByRole("img")).toBeVisible()
      await expect(article.getByRole("heading")).toBeVisible()
    }
    // Expect pagination controls to be displayed correctly
    const navigation = page.getByTestId("main-article-navigation")
    await expect(navigation).toBeVisible()
    await expect(navigation.getByTestId("prev-link")).toHaveCount(0)
    await expect(navigation.getByTestId("next-link")).not.toHaveClass(/disabled/)
    await expect(navigation.locator("li.active a")).toHaveText("1")
  })

  test("should display secondary news list", async ({page}) => {
    const secondaryArticles = page.getByTestId(/secondary-article-\d/)
    // Expect five secondary articles to be displayed
    await expect(secondaryArticles).toHaveCount(5)
    // Expect every article to have a title and no image
    for (const article of await secondaryArticles.all()) {
      await expect(article.getByRole("img")).toHaveCount(0)
      await expect(article.getByRole("heading")).toBeVisible()
    }
  })
})

test.describe("News Detail", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(testingUrl)
    await page.locator('#latest-article').click()
  })

  test("should render the article", async ({page}) => {
    await expect(page.getByTestId("article-title")).toBeVisible()
    await expect(page.getByTestId("article-image")).toBeVisible()
    await expect(page.getByTestId("article-body")).toBeVisible()
  })

  test.describe("Like Article", () => {

    test("should hide like button if not authenticated", async ({page}) => {
      await expect(page.getByTestId("like-article-form")).toHaveCount(0)
    })

    test("should allow like/unlike article button if authenticated", async ({page}) => {
      // Login and go to latest article
      await login(page)
      await page.locator('#latest-article').click()
      await expect(page.getByTestId("like-article-form")).toBeVisible()
      // Current like count and button text
      let initialCount = +(await page.getByTestId("number-of-likes").innerText()) || 0
      let initialText = await page.getByTestId("like-article-form").getByRole("button").innerText()
      // Click button twice, expect count and text to change each time
      for (let i = 0; i < 2; i++) {
        await Promise.all([
          page.waitForResponse(resp => resp.url().includes('/like') && resp.status() === 302),
          page.getByTestId("like-article-form").getByRole("button").click()
        ])
        const currentText = await page.getByTestId("like-article-form").getByRole("button").innerText()
        const currentCount = +(await page.getByTestId("number-of-likes").innerText())
        if (initialText.match(/Like this article/)) {
          expect(currentText).toMatch(/\d Like/)
          expect(currentCount).toBeGreaterThan(initialCount)
        } else {
          expect(currentText).toMatch(/Like this article/)
          expect(currentCount).toBeLessThan(initialCount)
        }
        initialCount = currentCount
        initialText = currentText
      }
    })
  })

})