from shared import InventoryForm
from big_five import BigFive
from core_self import CoreSelf

inventoryById = {0: BigFive, 1: CoreSelf}

for inventory_id, inventory in inventoryById.items():
    inventory.inventory_id = inventory_id
