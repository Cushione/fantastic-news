import { test, expect, Page } from '@playwright/test'
import { login } from './member.spec';

const testingUrl = process.env.TESTING_URL!

test.describe("Comment Section", () => {
  test.describe("Unauthenticated", () => {
    test.beforeEach(async ({ page }) => {
      await page.goto(testingUrl)
      await page.locator('#latest-article').click()
    })
  
    test("should render the comment section", async ({page}) => {
      await expect(page.getByTestId("comment-title")).toBeVisible()
      await expect(page.getByTestId("comment-list")).toHaveCount(1)
    })

    test("should hide the comment form if not authenticated", async ({page}) => {
      await expect(page.getByTestId("login-hint")).toBeVisible()
      await expect(page.getByTestId("comment-form")).toHaveCount(0)
    })

  })

  test.describe("Authenticated", () => {
    test.beforeEach(async ({ page }) => {
      await login(page)
      await page.goto(testingUrl)
      await page.locator('#latest-article').click()
    })
    
    test("should show the comment form if authenticated", async({page}) => {
      await expect(page.getByTestId("comment-form")).toBeVisible()
    })

    test("should be able to write comment", async({page}) => {
      const url = page.url()
      const count = await page.getByTestId("comment-list").locator(".card").count()
      await writeComment(page, "Test Comment")

      await expect(page).toHaveURL(url)
      expect(await page.getByTestId("comment-list").locator(".card").count()).toBeGreaterThan(count)
      const comment = page.getByTestId("comment-list").locator(".card").first()
      expect ((await comment.locator(".card-title").innerText()).trim()).toContain("test_user")
      expect ((await comment.locator(".comment-content").innerText()).trim()).toContain("Test Comment")
    })

    test("should be able to edit comment", async ({page}) => {
      await writeComment(page, "Test Comment")
      const comment = page.getByTestId("comment-list").locator(".card").first()
      await expect(comment.locator(".action-buttons")).toBeVisible()
      comment.locator(".action-buttons .comment-edit-btn").click()
      await expect(comment.getByRole("textbox")).toBeVisible()
      await comment.getByRole("textbox").clear()
      await comment.getByRole("textbox").fill("Changed Comment")
      await comment.locator(".comment-save-btn").click()
      await expect(comment.getByRole("textbox")).toHaveCount(0)
      expect ((await comment.locator(".comment-content").innerText()).trim()).toContain("Changed Comment")
    })

    test.describe("Delete comment", () => {

      test("should delete comment if confirmed", async ({page}) => {
        page.on('dialog', dialog => dialog.accept());
        await writeComment(page, "Test Comment")
        const comment = page.getByTestId("comment-list").locator(".card").first()
        await expect(comment.locator(".action-buttons")).toBeVisible()
        await Promise.all([
          page.waitForResponse(resp => resp.url().includes('/comments') && resp.status() === 200),
          comment.locator(".action-buttons .comment-delete-btn").click()
        ])
        await expect(comment.locator(".action-buttons .comment-delete-btn")).toHaveCount(0)
        expect ((await comment.locator(".comment-content").innerText()).trim()).toContain("This comment was deleted.")
      })

      test("should not delete comment if cancelled", async ({page}) => {
        page.on('dialog', dialog => dialog.dismiss());
        await writeComment(page, "Test Comment")
        const comment = page.getByTestId("comment-list").locator(".card").first()
        await expect(comment.locator(".action-buttons")).toBeVisible()
        await comment.locator(".action-buttons .comment-delete-btn").click()
        await expect(comment.locator(".action-buttons .comment-delete-btn i")).toHaveClass(/fa-trash-can/)
        expect ((await comment.locator(".comment-content").innerText()).trim()).toContain("Test Comment")
      })

    })
  })
})

async function writeComment(page: Page, content: string) {
  await Promise.all([
    page.waitForResponse(resp => resp.url().includes('/comment/') && resp.status() === 302),
    page.getByTestId("comment-form").getByRole("textbox").fill(content),
    page.getByTestId("comment-form").getByRole("button", {name: "Post Comment"}).click()
  ])
}