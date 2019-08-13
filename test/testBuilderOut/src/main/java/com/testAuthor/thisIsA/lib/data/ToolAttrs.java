package com.testAuthor.thisIsA.lib.data;

import com.testAuthor.thisIsA.CreativeTabGroups;
import net.minecraft.item.Item;


/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Object holding data for tool attributes. harvestLevelIn, maxUsesIn, efficiencyIn, maxDamageIn, enchantabilityIn is used
 * by ModItemTier
 */
public class ToolAttrs {

    private final Item.Properties itemProperties = new Item.Properties().group(CreativeTabGroups.ITEM_GROUP_TOOLS);
    private static final double NOT_SWORD_MODIFIER = 0.7;


    private final int attackDamageIn;
    private final float attackSpeedIn;

    // Used by ModItemTier
    private final int harvestLevelIn;
    private final int maxUsesIn;
    private final float efficiencyIn;
    private final float maxDamageIn;
    private final int enchantabilityIn;

    /**
     * Lazy constructor, use if you are hardcoding values for ModItemTier
     * @param attackDamageIn attack damage for sword
     * @param attackSpeedIn attack speed for sword
     */
    public ToolAttrs(final int attackDamageIn, final float attackSpeedIn) {
        this(attackDamageIn, attackSpeedIn, 0,0,0,0,0);
    }

    /**
     * Required if enumerating tools with different ModItemTier properties. Use getters to access these properties. eg.
     * getAttackDamageIn to get attackDamageIn
     * @param attackDamageIn attack damage for sword
     * @param attackSpeedIn attack speed for sword
     * @param harvestLevelIn int for harvest level wood is 0, stone 1, iron 2, and diamond 3
     * @param maxUsesIn number of blocks that can be broken wood is 59, diamond is approx 1500
     * @param efficiencyIn speed of block break diamond is around 10?
     * @param maxDamageIn ??? unknown effect
     * @param enchantabilityIn ??? unknown effect
     */
    public ToolAttrs(final int attackDamageIn, final float attackSpeedIn, final int harvestLevelIn, final int maxUsesIn,
                     final float efficiencyIn, final float maxDamageIn, final int enchantabilityIn) {
        this.attackDamageIn = attackDamageIn;
        this.attackSpeedIn = attackSpeedIn;
        this.harvestLevelIn = harvestLevelIn;
        this.maxUsesIn = maxUsesIn;
        this.efficiencyIn = efficiencyIn;
        this.maxDamageIn = maxDamageIn;
        this.enchantabilityIn = enchantabilityIn;
    }

    @SuppressWarnings("NumericCastThatLosesPrecision")
    public int getAttackDamageIn() {
        return (int)(attackDamageIn * NOT_SWORD_MODIFIER);
    }

    @SuppressWarnings("NumericCastThatLosesPrecision")
    public float getAttackSpeedIn() {
        return (float)(attackSpeedIn * NOT_SWORD_MODIFIER);
    }

    public int getSwordAttackDamageIn() {
        return attackDamageIn;
    }

    public float getSwordAttackSpeedIn() {
        return attackSpeedIn;
    }

    public Item.Properties getItemProperties() {
        return itemProperties;
    }

    public int getHarvestLevelIn() {
        return harvestLevelIn;
    }

    public int getMaxUsesIn() {
        return maxUsesIn;
    }

    public float getEfficiencyIn() {
        return efficiencyIn;
    }

    public float getMaxDamageIn() {
        return maxDamageIn;
    }

    public int getEnchantabilityIn() {
        return enchantabilityIn;
    }
}
