import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.notifications.services import create_notifications
from app.posts.selectors import get_post_selectors
from app.reaction.models import Reaction
from app.reaction.schema import ReactionResponse
from app.reaction.selectors import get_post_reaction_selectors,get_reactions_post_selectors
from app.users.models import User


async def toogle_reaction_services(post_id:uuid.UUID,db:AsyncSession, user:User):
    post = await get_post_selectors(post_id,db)
    reaction = await get_post_reaction_selectors(post.id,db,user)
    if reaction is None: # nếu chưa thả react thì tạo
        reaction = Reaction(
            user_id=user.id,
            post_id=post_id,
        )
        db.add(reaction)
        await db.commit()
        status = 'add'
        if post.user_id == user.id: # không thông báo cho mình nếu mình là chủ post thả cảm xúc
            await create_notifications(post.id, db, user)
    else:
        await db.delete(reaction)
        await db.commit()
        status = 'remove'
    return ReactionResponse(
        post_id = post.id,
        status=status,
    )

async def get_reactions_post_services(post_id:uuid.UUID, db:AsyncSession, user:User):
    post = await get_post_selectors(post_id,db)
    reactions = await get_reactions_post_selectors(post_id,db)
    return reactions
