package com.example.examplemod;


import net.minecraft.util.ResourceLocation;
import net.minecraftforge.fml.DistExecutor;
import net.minecraftforge.fml.ModContainer;
import net.minecraftforge.fml.ModList;
import net.minecraftforge.fml.common.Mod;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import javax.annotation.Nonnull;
import java.util.Optional;

// The value here should match an entry in the META-INF/mods.toml file
@Mod(Main.MOD_ID)
public class Main
{

    @SuppressWarnings("SpellCheckingInspection")
    public static final String MOD_ID = "examplemod";



    public static final Logger LOGGER = LogManager.getLogger();



    public Main() {
        // Create proxy instance. DistExecutor.runForDist also returns the created object, so you
        // could store that in a variable if you need it.
        // We cannot use method references here because it could load classes on invalid sides.
        //noinspection Convert2MethodRef
        DistExecutor.runForDist(
                () -> () -> new ServiceWorkers.Client(),
                () -> () -> new ServiceWorkers.Server()
        );
    }


    @SuppressWarnings("WeakerAccess")
    @Nonnull
    public static String getVersion() {
        final Optional<? extends ModContainer> o = ModList.get().getModContainerById(MOD_ID);
        if (o.isPresent()) {
            return o.get().getModInfo().getVersion().toString();
        }
        return "NONE";
    }


    /*
    Assumes dev if getVersion is none
     */
    public static boolean isDevBuild() {
        final String version = getVersion();
        return "NONE".equals(version);
    }


    @Nonnull
    public static ResourceLocation getId(final String path) {
        return new ResourceLocation(MOD_ID, path);
    }
}