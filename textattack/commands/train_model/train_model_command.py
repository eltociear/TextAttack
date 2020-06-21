import os
import datetime
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser

from textattack.commands import TextAttackCommand


class TrainModelCommand(TextAttackCommand):
    """
    The TextAttack train module:
    
        A command line parser to train a model from user specifications.
    """

    def run(self, args):
        
        date_now = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M")
        current_dir = os.path.dirname(os.path.realpath(__file__))
        outputs_dir = os.path.join(
            current_dir, os.pardir, os.pardir, os.pardir, "outputs", "training"
        )
        args.out_dir = os.path.normpath(outputs_dir)
        
        args.output_dir = os.path.join(root_output_dir, 
            f'{args.model}-{args.dataset}-{date_now}/')
        
        from .run_training import train_model
        train_model(args)

    @staticmethod
    def register_subcommand(main_parser: ArgumentParser):
        parser = main_parser.add_parser("train", help="train a model",
            formatter_class=ArgumentDefaultsHelpFormatter,)
        parser.add_argument('--model', type=str, required=True,
            help='directory of model to train',)
        parser.add_argument('--dataset', type=str, required=True,
            default='yelp', help='dataset for training; will be loaded from '
            '`nlp` library. if dataset has a subset, separate with a colon. '
            ' ex: `glue:sst2` or `rotten_tomatoes`')
        parser.add_argument('--tb_writer_step', type=int, default=1000, 
            help='Number of steps before writing to tensorboard')
        parser.add_argument('--checkpoint_steps', type=int, 
            default=5000, help='save model after this many steps')
        
        parser.add_argument('--checkpoint_every_epoch', action='store_true',
            default=False, help='save model checkpoint after each epoch')
        parser.add_argument('--num_train_epochs', '--epochs', type=int, 
            default=100, help='Total number of epochs to train for')
        parser.add_argument('--early_stopping_epochs', type=int, 
            default=-1, help='Number of epochs validation must increase'
                               ' before stopping early (-1 for no early stopping)')
        parser.add_argument('--batch_size', type=int, default=128, 
            help='Batch size for training')
        parser.add_argument('--max_length', type=int, default=512, 
            help='Maximum length of a sequence (anything beyond this will '
                 'be truncated)')
            
        parser.add_argument('--learning_rate', '--lr', type=int, default=2e-5, 
            help='Learning rate for Adam Optimization')
            
        parser.add_argument('--grad_accum_steps', type=int, default=1, 
            help='Number of steps to accumulate gradients before optimizing, '
                    'advancing scheduler, etc.')
            
        parser.add_argument('--warmup_proportion', type=int, default=0.1, 
            help='Warmup proportion for linear scheduling')
            
        parser.add_argument('--config_name', type=str, default='config.json', 
            help='Filename to save BERT config as')
            
        parser.add_argument('--weights_name', type=str, default='pytorch_model.bin', 
            help='Filename to save model weights as')
        
        parser.add_argument('--enable_wandb', default=False, action='store_true',
            help='log metrics to Weights & Biases')
        
        parser.set_defaults(func=TrainModelCommand())
