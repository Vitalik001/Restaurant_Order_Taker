import re
from app.src.guest.utils import GuestUtils


class GuestService:
    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()

    @staticmethod
    async def create_order():
        return await GuestUtils.create_order()

    @staticmethod
    async def handle_message(session_id: int, message: str):
        status = (await GuestUtils.get_status(session_id))["status"]
        if status == 1:
            await GuestUtils.save_message(session_id, message)
            return await GuestService.handle_state_1(session_id, message)
        elif status == 2:
            await GuestUtils.save_message(session_id, message)
            return await GuestService.handle_state_2(session_id, message)
        elif status == 3:
            await GuestUtils.save_message(session_id, message)
            return await GuestService.handle_state_3(session_id, message)
        elif status == 4:
            await GuestUtils.save_message(session_id, message)
            return await GuestService.handle_state_4(session_id, message)
        elif status == 5:
            await GuestUtils.save_message(session_id, message)
            return await GuestService.handle_state_5(session_id, message)
        else:
            return GuestService.handle_state_6()

    @staticmethod
    async def handle_state_1(session_id: int, message: str):
        if match := re.match(r"^i'd like (an? )?(.+?)(\.?)$", message, re.IGNORECASE):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            upsell = await GuestUtils.get_upsell()
            if item:
                if item["in_stock"] > 0:
                    await GuestUtils.add_item(session_id, item["id"])
                    # ordered upsell and in stock
                    if item["id"] == upsell["id"]:
                        await GuestUtils.set_status(session_id, 2)
                        return await GuestUtils.save_message(
                            session_id, "Would you like anything else?"
                        )
                    # ordered not upsell(in stock) but upsell in stock
                    elif upsell["in_stock"] > 0:
                        await GuestUtils.set_status(session_id, 5)
                        await GuestUtils.ask_upsell()
                        return await GuestUtils.save_message(
                            session_id,
                            f"Would you like to add a(an) {upsell['name']} for ${upsell['price']}.",
                        )
                    # ordered not upsell(in stock) but upsell not in stock
                    else:
                        await GuestUtils.set_status(session_id, 2)
                        return await GuestUtils.save_message(
                            session_id, "Would you like anything else?"
                        )
                else:
                    # ordered upsell but not in stock
                    if item["id"] == upsell["id"]:
                        await GuestUtils.set_status(session_id, 3)
                        return await GuestUtils.save_message(
                            session_id, f"I’m sorry but we’re out of {item_name}"
                        )
                    # ordered not upsell(not in stock) but upsell in stock
                    if upsell["in_stock"] > 0:
                        await GuestUtils.set_status(session_id, 4)
                        await GuestUtils.ask_upsell()
                        return await GuestUtils.save_message(
                            session_id,
                            f"I’m sorry but we’re out of {item_name}. Would you like to add a(an) {upsell['name']} for ${upsell['price']}.",
                        )
                    # not in stock upsell not in stock
                    await GuestUtils.set_status(session_id, 3)
                    return await GuestUtils.save_message(
                        session_id, f"I’m sorry but we’re out of {item_name}."
                    )

        return await GuestUtils.save_message(session_id, "I don't understand.")

    @staticmethod
    async def handle_state_2(session_id: int, message: str):
        if match := re.match(r"^i'd like (an? )?(.+?)(\.?)$", message, re.IGNORECASE):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                if item["in_stock"] > 0:
                    await GuestUtils.add_item(session_id, item["id"])
                    return await GuestUtils.save_message(
                        session_id, "Would you like anything else?"
                    )
                    # ordered not upsell(in stock) but upsell in stock
                else:
                    return await GuestUtils.save_message(
                        session_id, f"I’m sorry but we’re out of {item_name}."
                    )
        elif match := re.match(
            r"^i don't want (an? )?(.+?)(\.?)$", message, re.IGNORECASE
        ):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                number_of_items = await GuestUtils.remove_item(session_id, item["id"])
                if (
                    number_of_items is not None
                    and number_of_items["number_of_items"] >= 0
                ):
                    return await GuestUtils.save_message(
                        session_id,
                        f"{item_name} was removed. {item_name} left: {number_of_items['number_of_items']}.",
                    )
                else:
                    await GuestUtils.set_status(session_id, 3)
                    return await GuestUtils.save_message(
                        session_id, f"You don't have {item_name} in your order"
                    )

        elif re.match(r"^that's all(\.?)$", message, re.IGNORECASE):
            await GuestUtils.set_status(session_id, 6)
            order = await GuestUtils.get_order(session_id)
            return await GuestUtils.save_message(
                session_id,
                f"Your total is ${order['total_price']}. Thank you and have a nice day!",
            )
        return await GuestUtils.save_message(session_id, "I don't understand.")

    @staticmethod
    async def handle_state_3(session_id: int, message: str):
        if match := re.match(r"^i'd like (an? )?(.+?)(\.?)$", message, re.IGNORECASE):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                if item["in_stock"] > 0:
                    await GuestUtils.set_status(session_id, 2)
                    await GuestUtils.add_item(session_id, item["id"])
                    # ordered upsell and in stock
                    return await GuestUtils.save_message(
                        session_id, "Would you like anything else?"
                    )
                else:
                    return await GuestUtils.save_message(
                        session_id, f"I’m sorry but we’re out of {item_name}."
                    )
        return await GuestUtils.save_message(session_id, "I don't understand.")

    @staticmethod
    async def handle_state_4(session_id: int, message: str):
        if re.match(r"^yes,?( please(\.?))?$", message, re.IGNORECASE):
            # mark as accepted for upsell_stats
            await GuestUtils.accept_upsell()
            await GuestUtils.set_status(session_id, 2)
            upsell = await GuestUtils.get_upsell()

            await GuestUtils.add_item(session_id, upsell["id"])

            return await GuestUtils.save_message(
                session_id, "Would you like anything else?"
            )

        elif re.match(r"^no,?( thank you(\.?))?$", message, re.IGNORECASE):
            # mark as rejected for upsell_stats
            await GuestUtils.reject_upsell()
            await GuestUtils.set_status(session_id, 3)
            return await GuestUtils.save_message(
                session_id, "Would you like anything else?"
            )
        return await GuestUtils.save_message(session_id, "I don't understand.")

    @staticmethod
    async def handle_state_5(session_id: int, message: str):
        if re.match(r"^yes,?( please(\.?))?$", message, re.IGNORECASE):
            # mark as accepted for upsell_stats
            await GuestUtils.accept_upsell()
            await GuestUtils.set_status(session_id, 2)
            upsell = await GuestUtils.get_upsell()

            await GuestUtils.add_item(session_id, upsell["id"])

            return await GuestUtils.save_message(
                session_id, "Would you like anything else?"
            )

        elif re.match(r"^no,?( thank you(\.?))?$", message, re.IGNORECASE):
            # mark as rejected for upsell_stats
            await GuestUtils.reject_upsell()
            await GuestUtils.set_status(session_id, 2)
            return await GuestUtils.save_message(
                session_id, "Would you like anything else?"
            )

        elif re.match(r"^that's all(\.?)$", message, re.IGNORECASE):
            await GuestUtils.set_status(session_id, 6)
            order = await GuestUtils.get_order(session_id)
            return await GuestUtils.save_message(
                session_id,
                f"Your total is ${order['total_price']}. Thank you and have a nice day!",
            )
        return await GuestUtils.save_message(session_id, "I don't understand.")

    @staticmethod
    def handle_state_6():
        return {"message": "Your order is already completed"}
