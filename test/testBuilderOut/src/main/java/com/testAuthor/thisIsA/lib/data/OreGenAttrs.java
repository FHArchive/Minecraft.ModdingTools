package com.testAuthor.thisIsA.lib.data;

import net.minecraft.world.gen.placement.CountRangeConfig;

/**
 * @author FredHappyface
 * @version latest update 2019.07.18
 *
 * Object holding data for world gen. Uses a harvest level, CountRangeConfig and a veinSize
 */
public class OreGenAttrs {
    private final int harvestLevel;
    private final CountRangeConfig countRangeConfig;
    private final int veinSize;

    /**
     * Lazy constructor, use if you are happy with default ore clusters per chunk
     * @param harvestLevel pick level required to obtain tbe ore
     * @param veinSize number of ore in a vein
     */
    public OreGenAttrs(final int harvestLevel, final int veinSize){
        this(harvestLevel, new CountRangeConfig(15, 20,30, 50), veinSize);

    }

    /**
     *
     * @param harvestLevel pick level required to obtain tbe ore
     * @param countRangeConfig settings for the ore clusters in a chunk. Count - Number of clusters per chunk. BottomOffset -
     *                         Minimum y level. TopOffset - y = World surface - value?? INFO NEEDED. Maximum - Maximum y level
     * @param veinSize number of ore in a vein
     */
    @SuppressWarnings("WeakerAccess")
    public OreGenAttrs(final int harvestLevel, final CountRangeConfig countRangeConfig, final int veinSize){
        this.harvestLevel = harvestLevel;
        this.countRangeConfig = countRangeConfig;
        this.veinSize = veinSize;
    }

    public int getHarvestLevel() {
        return harvestLevel;
    }

    public CountRangeConfig getCountRangeConfig() {
        return countRangeConfig;
    }

    public int getVeinSize() {
        return veinSize;
    }
}
