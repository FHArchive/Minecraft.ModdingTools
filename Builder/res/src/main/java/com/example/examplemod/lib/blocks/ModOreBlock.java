package com.example.examplemod.lib.blocks;

import net.minecraft.block.BlockState;
import net.minecraft.block.material.Material;
import net.minecraft.util.math.BlockPos;
import net.minecraft.util.math.MathHelper;
import net.minecraft.world.IWorldReader;

/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Custom ore block with custom implementation of get exp and get harvest level
 */
public class ModOreBlock extends net.minecraft.block.OreBlock {
    private final int harvestLevel;


    /**
     * Define an ModOreBlock
     * @param harvestLevel level of tool required to obtain ore
     */
    public ModOreBlock(final int harvestLevel) {
        this(Properties.create(Material.ROCK).hardnessAndResistance(3, 3), harvestLevel);

    }

    @SuppressWarnings("WeakerAccess")
    public ModOreBlock(final Properties builder, final int harvestLevel) {
        super(builder);
        this.harvestLevel = harvestLevel;
    }

    @Override
    public int getExpDrop(final BlockState state, final IWorldReader reader, final BlockPos pos, final int fortune, final int silktouch) {
        return silktouch == 0 ? MathHelper.nextInt(RANDOM, 1, 5) : 0;
    }


    @Override
    public int getHarvestLevel(final BlockState state) {
        return this.harvestLevel;
    }

    
}