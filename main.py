
"""
Minecraft AI Cloud Player - Main Controller
Run this from GitHub Codespaces or Colab
"""
import os
import sys
import asyncio
from typing import Optional
import logging
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.cloud_config import CloudConfig
from core.cloud_screen_capturer import CloudScreenCapturer
from core.cloud_game_controller import CloudGameController
from core.cloud_vision_processor import CloudVisionProcessor
from core.cloud_decision_maker import CloudDecisionMaker
from ui.cloud_dashboard import CloudDashboard

class MinecraftAICloud:
    def __init__(self, config_path: Optional[str] = None):
        """Initialize cloud-based Minecraft AI"""
        self.config = CloudConfig(config_path)
        self.setup_logging()
        
        # Initialize components
        self.capturer = CloudScreenCapturer(self.config)
        self.controller = CloudGameController(self.config)
        self.vision = CloudVisionProcessor(self.config)
        self.decision_maker = CloudDecisionMaker(self.config)
        self.dashboard = CloudDashboard(self.config)
        
        self.running = False
        self.task = None
        
        print("🌤️  Minecraft AI Cloud Initialized")
        print(f"📊 Dashboard: {self.config.DASHBOARD_URL}")
        print(f"🎮 Control Panel: {self.config.CONTROL_PANEL_URL}")
    
    def setup_logging(self):
        """Setup cloud logging"""
        log_dir = Path(self.config.LOGS_DIR)
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'minecraft_ai.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    async def start(self):
        """Start the AI player"""
        self.running = True
        self.logger.info("🚀 Starting Minecraft AI Cloud Player")
        
        try:
            # Start dashboard
            await self.dashboard.start()
            
            # Start capture
            self.capturer.start()
            
            # Main AI loop
            while self.running:
                # Get latest frame
                frame = self.capturer.get_latest_frame()
                
                if frame is not None:
                    # Process vision
                    game_state = self.vision.process_frame(frame)
                    
                    # Update dashboard
                    await self.dashboard.update(game_state)
                    
                    # Make decisions
                    actions = self.decision_maker.decide(game_state)
                    
                    # Execute actions
                    for action in actions:
                        await self.controller.execute(action)
                
                # Control loop speed
                await asyncio.sleep(1 / self.config.FPS)
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Received interrupt, shutting down...")
        except Exception as e:
            self.logger.error(f"❌ Error in main loop: {e}")
        finally:
            await self.stop()
    
    async def stop(self):
        """Stop the AI player"""
        self.running = False
        self.logger.info("🛑 Stopping Minecraft AI Cloud Player")
        
        if self.capturer:
            self.capturer.stop()
        
        if self.dashboard:
            await self.dashboard.stop()
        
        self.logger.info("✅ Shutdown complete")
    
    def run(self):
        """Run the AI player (blocking)"""
        try:
            asyncio.run(self.start())
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description='Minecraft AI Cloud Player')
    parser.add_argument('--config', type=str, help='Path to config file')
    parser.add_argument('--dashboard', action='store_true', help='Start dashboard only')
    parser.add_argument('--train', action='store_true', help='Train models')
    args = parser.parse_args()
    
    # Create and run AI
    ai = MinecraftAICloud(args.config)
    
    if args.dashboard:
        # Start only dashboard
        asyncio.run(ai.dashboard.start())
    elif args.train:
        # Train models
        from trainers.cloud_trainer import CloudTrainer
        trainer = CloudTrainer(ai.config)
        trainer.train()
    else:
        # Run full AI
        ai.run()
