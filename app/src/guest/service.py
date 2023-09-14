from typing import List
import re
from app.src.guest.utils import GuestUtils
from app.src.models.item import Item


class GuestService:
    @staticmethod
    async def get_menu():
        return await GuestUtils.get_menu()

    # @staticmethod
    # async def add_items(order_id: int, item: List[Item]):
    #     return await GuestUtils.add_items(order_id, item)
    #
    # @staticmethod
    # async def check_item(item_name: str):
    #     return await GuestUtils.check_item(item_name)
    #
    @staticmethod
    async def get_upsell():
        return await GuestUtils.get_upsell()

    @staticmethod
    async def create_order():
        return await GuestUtils.create_order()

    @staticmethod
    async def handle_message(session_id: int, message: str):
        if match := re.match(r"^i'd like (an? )?(.+)$", message, re.IGNORECASE):
            item_name = match.group(2)
            item = await GuestUtils.check_item(item_name)
            if item:
                item_id = item[0]["id"]
                await GuestUtils.add_item(session_id, item_id)
                upsell = (await GuestUtils.get_upsell())

                # if selected item is an upsell do not recommend it
                if item_id == upsell['id']:
                    await GuestUtils.set_upsell(session_id)

                # # if upsell was not recommend, recommend it
                if not (await GuestUtils.check_order_upsell(session_id))["upsell"]:
                    await GuestUtils.set_upsell(session_id)
                    return await GuestUtils.save_message(session_id, f"- Would you like to add a {upsell['name']} for ${upsell['price']}?")

                return await GuestUtils.save_message(session_id, "- Would you like anything else?")
        return await GuestUtils.save_message(session_id, "- I don't understand")


    # def generate_bot_response(self, user_input):
    #     if match:=re.match(r"^i'd like (an? )?(.+)$", user_input, re.IGNORECASE):
    #         item_name = match.group(2)
    #         if id:=self.check_item(item_name):
    #             self.order[id] = self.order.setdefault(id, 0) + 1
    #
    #             # if selected item is an upsell do not recommend it
    #             if id == self.upsell['id']:
    #                 self.upsell_recommended = True
    #
    #             # if upsell was not recommend, recommend it
    #             if not self.upsell_recommended:
    #                 self.upsell_recommended = True
    #                 return f"Bot: - Would you like to add a {self.upsell['name']} for ${self.upsell['price']}?"
    #
    #             return "Bot: - Would you like anything else?"
    #
    #     elif re.match(r"yes, please$", user_input, re.IGNORECASE):
    #         self.order[self.upsell['id']] = 1
    #         return "Bot: - Would you like anything else?"
    #
    #     elif re.match(r"no, thank you$", user_input, re.IGNORECASE):
    #         return "Bot: - Would you like anything else?"
    #
    #     elif match:=re.match(r"i don't want (an? )?(.+)$", user_input, re.IGNORECASE):
    #         item_name = match.group(2)
    #         if id:=self.check_item(item_name):
    #             self.order.pop(id)
    #             return "Bot: - Would you like anything else?"
    #
    #
    #     elif user_input == "That's all":
    #         return self.add_order()
    #
    #     return "Bot: - I don't understand"




