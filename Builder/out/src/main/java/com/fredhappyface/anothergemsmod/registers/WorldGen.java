package com.fredhappyface.anothergemsmod.registers;


import net.minecraft.world.biome.Biome;
import net.minecraft.world.gen.GenerationStage;
import net.minecraft.world.gen.feature.Feature;
import net.minecraft.world.gen.feature.OreFeatureConfig;
import net.minecraft.world.gen.placement.Placement;
import net.minecraftforge.common.BiomeManager;



public class WorldGen {


    public static void setupOreGeneration() {
        for (BiomeManager.BiomeType btype : BiomeManager.BiomeType.values()) {
            for (final BiomeManager.BiomeEntry biomeEntry : BiomeManager.getBiomes(btype)) {

                biomeEntry.biome.addFeature(GenerationStage.Decoration.UNDERGROUND_ORES, Biome.createDecoratedFeature(Feature.ORE, new OreFeatureConfig(OreFeatureConfig.FillerBlockType.NATURAL_STONE,
                        DefaultState, VeinSize, Placement.COUNT_RANGE, CountRangeConfig)));

            


            }
        }
    }



}

