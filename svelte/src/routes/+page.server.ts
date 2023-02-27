import type { PageServerLoad } from "./$types"
import { PrismaClient } from "@prisma/client"

const prisma = new PrismaClient()

export const load: PageServerLoad = async () => {
  const users = prisma.user.findMany({ include: { posts: true } })
  const posts = prisma.post.findMany({ include: { author: true } })

  return { users, posts }
}
