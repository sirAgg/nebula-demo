import demo, nmath, imgui
import enum

class ItemType(enum.auto):
    LOG         = 0
    IRON_ORE    = 1
    IRON_INGOT  = 2
    SWORD       = 3

class ItemStack:
    logs       = 0
    ironores   = 0
    ironingots = 0
    swords     = 0

    def __init__(self, x, y):
        self.entity = demo.SpawnEntity("StaticEnvironment/knob_plastic")
        self.entity.WorldTransform = nmath.Mat4.scaling(3,3,3) * nmath.Mat4.translation(x, 0.0, y)

    def is_empty(self):
        return  self.logs <= 0 and \
                self.ironores <= 0 and \
                self.ironingots <= 0 and \
                self.swords <= 0

    def delete(self):
        demo.Delete(self.entity)


class ItemManager:
    def __init__(self):
        self.global_logs        = 0
        self.global_ironores    = 0
        self.global_ironingots  = 0
        self.global_sword       = 0
        self.global_charcoal    = 0
        self.item_map = {}
    

    def add_item(self, x, y, item_type: ItemType):
        item_stack = self.item_map.get((x,y))
        if item_stack == None:
            item_stack = ItemStack(x,y)
            self.item_map[(x,y)] = item_stack

        if item_type == ItemType.LOG:
            item_stack.logs += 1
            self.global_logs += 1

        elif item_type == ItemType.IRON_ORE:
            item_stack.ironores += 1
            self.global_ironores += 1

        elif item_type == ItemType.IRON_INGOT:
            item_stack.ironingots += 1
            self.global_ironingots += 1

        elif item_type == ItemType.SWORD:
            item_stack.swords += 1
            self.global_swords += 1


    def remove_item(self, x, y, item_type: ItemType):
        item_stack = self.item_map.get((x,y))
        if item_stack == None:
            return False


        if item_type == ItemType.LOG:
            if item_stack.logs <= 0:
                return False
            item_stack.logs -= 1
            self.global_logs -= 1

        elif item_type == ItemType.IRON_ORE:
            if item_stack.ironores <= 0:
                return False
            item_stack.ironores -= 1
            self.global_ironores -= 1

        elif item_type == ItemType.IRON_INGOT:
            if item_stack.ironingots <= 0:
                return False
            item_stack.ironingots -= 1
            self.global_ironingots -= 1

        elif item_type == ItemType.SWORD:
            if item_stack.swords <= 0:
                return False
            item_stack.swords -= 1
            self.global_swords -= 1

        if item_stack.is_empty():
            item_stack.delete()
            self.item_map.pop((x,y))

        return True

    def get_n_items(self, x, y, item_type: ItemType):
        item_stack = self.item_map.get((x,y))
        if item_stack == None:
            return 0


        if item_type == ItemType.LOG:
            return item_type.log

        elif item_type == ItemType.IRON_ORE:
            return item_type.ironores

        elif item_type == ItemType.IRON_INGOT:
            return item_type.ironingots

        elif item_type == ItemType.SWORD:
            return item_type.swords

        return 0

    def get_global_n_items(self, item_type: ItemType):
        
        if item_type == ItemType.LOG:
            return self.global_logs

        elif item_type == ItemType.IRON_ORE:
            return self.global_ironores

        elif item_type == ItemType.IRON_INGOT:
            return self.global_ironingots

        elif item_type == ItemType.SWORD:
            return self.global_swords


    
    def add_charcoal(self, x, y):
        self.global_charcoal += 1

    def remove_charcoal(self, x, y):
        self.global_charcoal -= 1
    
    def get_n_charcoals(self, x, y):
        self.global_charcoal -= 1

    def is_there_items_at(self, x, y):
        return self.item_map.get((x,y)) != None

    def draw_hover(self, x, y):
        imgui.Begin("ItemOnGround", None, 0)
        try:
            members = [(attr, getattr(self,attr)) for attr in dir(self) if not callable(getattr(self,attr)) and not attr.startswith("__") and not attr == "item_map"]
            for member, value in members:
                imgui.Text(member + ": " + str(value))

            imgui.Text("---------------------")

            item_stack = self.item_map.get((x,y))
            if item_stack == None:
                imgui.Text("No Items.")
            else:
                members = [(attr, getattr(item_stack,attr)) for attr in dir(item_stack) if not callable(getattr(item_stack,attr)) and not attr.startswith("__") and not attr == "entity"]
            
                for member, value in members:
                    imgui.Text(member + ": " + str(value))

            imgui.End()

        except Exception as e:
            imgui.End()
            raise e


manager = ItemManager()
