from .shared import InventoryForm

from .big_five import BigFive
from .core_self import CoreSelf
from .career_commitment import CareerCommitment
from .ambiguity import Ambiguity
from .firo_b import FiroB
from .via import Via

inventory_cls_list = (
    BigFive, CoreSelf, CareerCommitment,
    Ambiguity, FiroB, Via
)

numeric_inventory_cls_list = (
    BigFive, CoreSelf, CareerCommitment,
    Ambiguity, FiroB
)

inventory_by_id = dict(zip(range(len(inventory_cls_list)), inventory_cls_list))

for inventory_id, inventory in inventory_by_id.items():
    inventory.inventory_id = inventory_id
