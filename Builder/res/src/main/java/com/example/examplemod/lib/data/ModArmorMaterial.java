package com.example.examplemod.lib.data;

import net.minecraft.inventory.EquipmentSlotType;
import net.minecraft.item.IArmorMaterial;
import net.minecraft.item.crafting.Ingredient;
import net.minecraft.util.LazyLoadBase;
import net.minecraft.util.SoundEvent;
import net.minecraft.util.SoundEvents;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.api.distmarker.OnlyIn;

import java.util.Arrays;
import java.util.function.Supplier;

/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Set the properties of modded armor eg. new ModArmorMaterial("diamond", 33, new int[]{3, 6, 8, 3}, 10, SoundEvents.ITEM_ARMOR_EQUIP_DIAMOND, 2.0F, () -> {
 *       return Ingredient.fromItems(Items.DIAMOND);for diamond armor
 */
public class ModArmorMaterial implements IArmorMaterial {
    private static final int[] MAX_DAMAGE_ARRAY = {13, 15, 16, 11};
    private final String name;
    private final int maxDamageFactor;
    private final int[] damageReductionAmountArray;
    private final int enchantability;
    private final SoundEvent soundEvent;
    private final float toughness;
    private final LazyLoadBase<Ingredient> repairMaterial;


    // eg ModArmorMaterial("diamond", 33, new int[]{3, 6, 8, 3}, 10, SoundEvents.ITEM_ARMOR_EQUIP_DIAMOND, 2.0F, () -> {
    //      return Ingredient.fromItems(Items.DIAMOND);
    //   }),

    /**
     * @param name required to load the texture (must add!)
     * @param maxDamageFactor number of hits or used to derive said value?
     * @param damageReductionArray number of hp to reduce damage by
     * @param enchantability same as for tools
     * @param toughness ???
     * @param repairMaterial Ingredient.fromItems(ITEM)
     */
    public ModArmorMaterial(final String name, final int maxDamageFactor, final int[] damageReductionArray, final int enchantability, final float toughness, final Supplier<Ingredient>  repairMaterial) {
        this(name, maxDamageFactor, damageReductionArray, enchantability, SoundEvents.ITEM_ARMOR_EQUIP_GOLD,toughness, repairMaterial);
    }

    @SuppressWarnings("WeakerAccess")
    public ModArmorMaterial(final String nameIn, final int maxDamageFactor, final int[] damageReductionArray, final int enchantability, final SoundEvent soundEvent, final float toughness, final Supplier<Ingredient> repairMaterial) {
        this.name = nameIn;
        this.maxDamageFactor = maxDamageFactor;
        this.damageReductionAmountArray = Arrays.copyOf(damageReductionArray, damageReductionArray.length);
        this.enchantability = enchantability; // same as for tools
        this.soundEvent = soundEvent;
        this.toughness = toughness;
        this.repairMaterial = new LazyLoadBase<>(repairMaterial);
    }

    public int getDurability(final EquipmentSlotType slotIn) {
        return MAX_DAMAGE_ARRAY[slotIn.getIndex()] * this.maxDamageFactor;
    }

    public int getDamageReductionAmount(final EquipmentSlotType slotIn) {
        return this.damageReductionAmountArray[slotIn.getIndex()];
    }

    public int getEnchantability() {
        return this.enchantability;
    }

    public SoundEvent getSoundEvent() {
        return this.soundEvent;
    }

    public Ingredient getRepairMaterial() {
        return this.repairMaterial.getValue();
    }

    @OnlyIn(Dist.CLIENT)
    public String getName() {
        return this.name;
    }

    public float getToughness() {
        return this.toughness;
    }
}
