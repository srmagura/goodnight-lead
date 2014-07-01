from shared import InventoryForm

from big_five import BigFive
from core_self import CoreSelf
from career_commitment import CareerCommitment
from ambiguity import Ambiguity
from firo_b import FiroB

inventory_by_id = {0: BigFive, 1: CoreSelf, 2: CareerCommitment,
    3: Ambiguity, 4: FiroB}

for inventory_id, inventory in inventory_by_id.items():
    inventory.inventory_id = inventory_id
