package com.fredhappyface.anothergemsmod.lib.data;

import com.fredhappyface.anothergemsmod.CreativeTabGroups;
import net.minecraft.item.Item;

import java.util.Arrays;

/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Object holding data for armor attributes
 */
public class ArmorAttrs {

    private final Item.Properties itemProperties = new Item.Properties().group(CreativeTabGroups.ITEM_GROUP_ARMOUR);


    private final int maxDamageFactor;
    private final int[] damageReductionAmountArray;
    private final float toughness;

    /**
     *
     * @param maxDamageFactor number of hits or used to derive said value?
     * @param damageReductionArray number of hp to reduce damage by
     * @param toughness ???
     */
    public ArmorAttrs(final int maxDamageFactor, final int[] damageReductionArray, final float toughness) {
        this.maxDamageFactor = maxDamageFactor;
        this.damageReductionAmountArray = Arrays.copyOf(damageReductionArray, damageReductionArray.length);
        this.toughness = toughness;
    }

    public int getMaxDamageFactor() {
        return maxDamageFactor;
    }

    public int[] getDamageReductionAmountArray() {
        return Arrays.copyOf(damageReductionAmountArray, damageReductionAmountArray.length);
    }

    public float getToughness() {
        return toughness;
    }

    public Item.Properties getItemProperties(){
        return itemProperties;
    }
}
