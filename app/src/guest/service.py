import re
from app.src.guest.utils import GuestUtils


class GuestService:
    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()

    @staticmethod
    async def get_upsell():
        return await GuestUtils.get_upsell()

    @staticmethod
    async def create_order():
        return await GuestUtils.create_order()

    @staticmethod
    async def handle_message(session_id: int, message: str):
        await GuestUtils.save_message(session_id, message)
        if match := re.match(r"^i'd like (an? )?(.+?)(\.?)$", message, re.IGNORECASE):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                await GuestUtils.add_item(session_id, item["id"])
                upsell = await GuestUtils.get_upsell()

                # if selected item is an upsell do not recommend it
                if item["id"] == upsell["id"]:
                    await GuestUtils.set_upsell(session_id)

                # # if upsell was not recommend, recommend it
                if not (await GuestUtils.check_order_upsell(session_id))["upsell"]:
                    # mark that upsell was recommended
                    await GuestUtils.set_upsell(session_id)

                    # mark as asked for upsell_stats
                    await GuestUtils.ask_upsell()
                    return await GuestUtils.save_message(
                        session_id,
                        f"Would you like to add a(an) {upsell['name']} for ${upsell['price']}?",
                    )

                return await GuestUtils.save_message(
                    session_id, "Would you like anything else?"
                )

            return await GuestUtils.save_message(session_id, "I don't understand")

        elif re.match(r"^yes,?( please(\.?))?$", message, re.IGNORECASE):
            # mark as accepted for upsell_stats
            await GuestUtils.accept_upsell()

            upsell = await GuestUtils.get_upsell()
            await GuestUtils.add_item(session_id, upsell["id"])

            return await GuestUtils.save_message(
                session_id, "Would you like anything else?"
            )

        elif re.match(r"^no,?( thank you(\.?))?$", message, re.IGNORECASE):
            # mark as rejected for upsell_stats
            await GuestUtils.reject_upsell()
            return await GuestUtils.save_message(
                session_id, "- Would you like anything else?"
            )

        elif match := re.match(
            r"^i don't want (an? )?(.+?)(\.?)$", message, re.IGNORECASE
        ):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                await GuestUtils.remove_item(session_id, item["id"])
                return await GuestUtils.save_message(
                    session_id, "Would you like anything else?"
                )
            return await GuestUtils.save_message(session_id, "I don't understand")

        elif re.match(r"^that's all(\.?)$", message, re.IGNORECASE):
            order = await GuestUtils.set_completed(session_id)
            return await GuestUtils.save_message(
                session_id,
                f"Your total is ${order['total_price']}. Thank you and have a nice day!",
            )

        return await GuestUtils.save_message(session_id, "I don't understand.")
