package com.example.examplemod;


import com.example.examplemod.registers.ModBlocks;
import com.example.examplemod.registers.ModItems;
import com.example.examplemod.registers.WorldGen;
import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.DeferredWorkQueue;
import net.minecraftforge.fml.event.lifecycle.*;
import net.minecraftforge.fml.event.server.FMLServerStartingEvent;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;


/**
 * ServiceWorkers allows client and server code to be separated, while executing common code on both
 * sides. There are two nested classes, {@link Client} and {@link Server}.
 */
class ServiceWorkers {
    ServiceWorkers() {
        // Register the setup, enqueueIMC, and processIMC methods for modloading
        FMLJavaModLoadingContext.get().getModEventBus().addListener(ServiceWorkers::commonSetup);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(ServiceWorkers::enqueueIMC);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(ServiceWorkers::processIMC);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(ModBlocks::registerAll);
        FMLJavaModLoadingContext.get().getModEventBus().addListener(ModItems::registerAll);

        // Register ourselves for server and other game events we are interested in
        MinecraftForge.EVENT_BUS.register(this);
    }

    @SuppressWarnings("unused")
    private static void commonSetup(final FMLCommonSetupEvent event) {
        DeferredWorkQueue.runLater(WorldGen::setupOreGeneration);
    }

    @SuppressWarnings("unused")
    private static void enqueueIMC(final InterModEnqueueEvent event) {
    }

    @SuppressWarnings("unused")
    private static void processIMC(final InterModProcessEvent event) {
    }

    @SubscribeEvent @SuppressWarnings("unused")
    public void serverStarting(final FMLServerStartingEvent event) {
    }

    /*
    Client only
     */
    static class Client extends ServiceWorkers {
        Client() {
            FMLJavaModLoadingContext.get().getModEventBus().addListener(Client::clientSetup);
        }

        @SuppressWarnings("unused")
        private static void clientSetup(final FMLClientSetupEvent event) {
        }
    }

    /*
    Server only
     */
    static class Server extends ServiceWorkers {
        Server() {
            FMLJavaModLoadingContext.get().getModEventBus().addListener(Server::serverSetup);
        }

        @SuppressWarnings("unused")
        private static void serverSetup(final FMLDedicatedServerSetupEvent event) {
        }
    }
}