package com.fredhappyface.anothergemsmod.registers;

import com.fredhappyface.anothergemsmod.Main;
import net.minecraft.item.BlockItem;
import net.minecraft.item.Item;
import net.minecraft.util.ResourceLocation;
import net.minecraftforge.event.RegistryEvent;
import net.minecraftforge.registries.ForgeRegistries;

import java.util.LinkedHashMap;
import java.util.Map;

public class ModItems {


    @SuppressWarnings("CollectionWithoutInitialCapacity")
    static final Map<String, BlockItem> BLOCKS_TO_REGISTER = new LinkedHashMap<>();


    // Namespaces
    private static final String TOOLS  = "tools/";
    private static final String ARMOUR  = "armor/";

    public static void registerAll(final RegistryEvent.Register<Item> event){

        if (!event.getName().equals(ForgeRegistries.ITEMS.getRegistryName())) {
            return;
        }



        // Blocks
        BLOCKS_TO_REGISTER.forEach(ModItems::register);


        // Items
        
    }



    /**
     * Register an item to the creative mode tab and to the game
     * @param name name of the item (unlocalized)
     * @param item the item object
     * @return item
     */
    @SuppressWarnings("UnusedReturnValue")
    private static <T extends Item> T register(final String name, final T item){
        final ResourceLocation resourceId = Main.getId(name);
        item.setRegistryName(resourceId);
        ForgeRegistries.ITEMS.register(item);
        return item;

    }

}