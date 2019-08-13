package com.testAuthor.thisIsA.lib.data;

import net.minecraft.item.IItemTier;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.util.LazyLoadBase;

import java.util.function.Supplier;




/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Set the tier of a modded item eg. new ModItemTier(3, 1561, 8.0F, 3.0F, 10, () -> {
 *       return Ingredient.fromItems(Items.DIAMOND); for a diamond tool
 */
public class ModItemTier implements IItemTier{

    private final int harvestLevel;
    private final int maxUses;
    private final float efficiency;
    private final float attackDamage;
    private final int enchantability;
    private final LazyLoadBase<Ingredient> repairMaterial;

    /**
     *
     * @param harvestLevelIn int for harvest level wood is 0, stone 1, iron 2, and diamond 3
     * @param maxUsesIn number of blocks that can be broken wood is 59, diamond is approx 1500
     * @param efficiencyIn speed of block break diamond is around 10?
     * @param attackDamageIn attack damage for sword ???
     * @param enchantabilityIn ??? unknown effect
     * @param repairMaterialIn Ingredient.fromItems(ITEM)
     */
    public ModItemTier(final int harvestLevelIn, final int maxUsesIn, final float efficiencyIn, final float attackDamageIn, final int enchantabilityIn, final Supplier<Ingredient> repairMaterialIn) {
        this.harvestLevel = harvestLevelIn;
        this.maxUses = maxUsesIn;
        this.efficiency = efficiencyIn;
        this.attackDamage = attackDamageIn;
        this.enchantability = enchantabilityIn;
        this.repairMaterial = new LazyLoadBase<>(repairMaterialIn);
    }

    public int getMaxUses() {
        return this.maxUses;
    }

    public float getEfficiency() {
        return this.efficiency;
    }

    public float getAttackDamage() {
        return this.attackDamage;
    }

    public int getHarvestLevel() {
        return this.harvestLevel;
    }

    public int getEnchantability() {
        return this.enchantability;
    }

    public Ingredient getRepairMaterial() {
        return this.repairMaterial.getValue();
    }
}
