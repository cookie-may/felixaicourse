// Auto-generated data - all 20 phases with 272+ lessons
// Source: https://github.com/rohitg00/ai-engineering-from-scratch

export interface Lesson {
  name: string;
  status: 'complete' | 'planned' | 'in-progress';
  type: string;
  lang: string;
  url?: string;
  path?: string; // Internal path for lesson viewer: "phase-slug/lesson-slug"
}

export interface Phase {
  id: number;
  name: string;
  status: 'complete' | 'planned' | 'in-progress';
  desc: string;
  lessons: Lesson[];
}

export const PHASES: Phase[] = [
  {
    id: 0,
    name: "Setup & Tooling",
    status: "complete",
    desc: "🛠️ *Get your environment ready for everything that follows.*",
    lessons: [
      { name: "Dev Environment", status: "complete", type: "Build", lang: "Python, TypeScript, Rust", path: "phases/00-setup-and-tooling/01-dev-environment" },
      { name: "Git & Collaboration", status: "complete", type: "Learn", lang: "—", path: "phases/00-setup-and-tooling/02-git-and-collaboration" },
      { name: "GPU Setup & Cloud", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/03-gpu-setup-and-cloud" },
      { name: "APIs & Keys", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/00-setup-and-tooling/04-apis-and-keys" },
      { name: "Jupyter Notebooks", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/05-jupyter-notebooks" },
      { name: "Python Environments", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/06-python-environments" },
      { name: "Docker for AI", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/07-docker-for-ai" },
      { name: "Editor Setup", status: "complete", type: "Build", lang: "—", path: "phases/00-setup-and-tooling/08-editor-setup" },
      { name: "Data Management", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/09-data-management" },
      { name: "Terminal & Shell", status: "complete", type: "Learn", lang: "—", path: "phases/00-setup-and-tooling/10-terminal-and-shell" },
      { name: "Linux for AI", status: "complete", type: "Learn", lang: "—", path: "phases/00-setup-and-tooling/11-linux-for-ai" },
      { name: "Debugging & Profiling", status: "complete", type: "Build", lang: "Python", path: "phases/00-setup-and-tooling/12-debugging-and-profiling" }
    ]
  },
  {
    id: 1,
    name: "Math Foundations",
    status: "complete",
    desc: "The intuition behind every AI algorithm, through code.",
    lessons: [
      { name: "Linear Algebra Intuition", status: "complete", type: "Learn", lang: "Python, Julia", path: "phases/01-math-foundations/01-linear-algebra-intuition" },
      { name: "Vectors, Matrices & Operations", status: "complete", type: "Build", lang: "Python, Julia", path: "phases/01-math-foundations/02-vectors-matrices-operations" },
      { name: "Matrix Transformations & Eigenvalues", status: "complete", type: "Build", lang: "Python, Julia", path: "phases/01-math-foundations/03-matrix-transformations" },
      { name: "Calculus for ML: Derivatives & Gradients", status: "complete", type: "Learn", lang: "Python", path: "phases/01-math-foundations/04-calculus-for-ml" },
      { name: "Chain Rule & Automatic Differentiation", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/05-chain-rule-and-autodiff" },
      { name: "Probability & Distributions", status: "complete", type: "Learn", lang: "Python", path: "phases/01-math-foundations/06-probability-and-distributions" },
      { name: "Bayes' Theorem & Statistical Thinking", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/07-bayes-theorem" },
      { name: "Optimization: Gradient Descent Family", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/08-optimization" },
      { name: "Information Theory: Entropy, KL Divergence", status: "complete", type: "Learn", lang: "Python", path: "phases/01-math-foundations/09-information-theory" },
      { name: "Dimensionality Reduction: PCA, t-SNE, UMAP", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/10-dimensionality-reduction" },
      { name: "Singular Value Decomposition", status: "complete", type: "Build", lang: "Python, Julia", path: "phases/01-math-foundations/11-singular-value-decomposition" },
      { name: "Tensor Operations", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/12-tensor-operations" },
      { name: "Numerical Stability", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/13-numerical-stability" },
      { name: "Norms & Distances", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/14-norms-and-distances" },
      { name: "Statistics for ML", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/15-statistics-for-ml" },
      { name: "Sampling Methods", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/16-sampling-methods" },
      { name: "Linear Systems", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/17-linear-systems" },
      { name: "Convex Optimization", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/18-convex-optimization" },
      { name: "Complex Numbers for AI", status: "complete", type: "Learn", lang: "Python", path: "phases/01-math-foundations/19-complex-numbers" },
      { name: "The Fourier Transform", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/20-fourier-transform" },
      { name: "Graph Theory for ML", status: "complete", type: "Build", lang: "Python", path: "phases/01-math-foundations/21-graph-theory" },
      { name: "Stochastic Processes", status: "complete", type: "Learn", lang: "Python", path: "phases/01-math-foundations/22-stochastic-processes" }
    ]
  },
  {
    id: 2,
    name: "ML Fundamentals",
    status: "complete",
    desc: "Classical ML — still the backbone of most production AI.",
    lessons: [
      { name: "What Is Machine Learning", status: "complete", type: "Learn", lang: "Python", path: "phases/02-ml-fundamentals/01-what-is-machine-learning" },
      { name: "Linear Regression from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/02-linear-regression" },
      { name: "Logistic Regression & Classification", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/03-logistic-regression" },
      { name: "Decision Trees & Random Forests", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/04-decision-trees" },
      { name: "Support Vector Machines", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/05-support-vector-machines" },
      { name: "KNN & Distance Metrics", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/06-knn-and-distances" },
      { name: "Unsupervised Learning: K-Means, DBSCAN", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/07-unsupervised-learning" },
      { name: "Feature Engineering & Selection", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/08-feature-engineering" },
      { name: "Model Evaluation: Metrics, Cross-Validation", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/09-model-evaluation" },
      { name: "Bias, Variance & the Learning Curve", status: "complete", type: "Learn", lang: "Python", path: "phases/02-ml-fundamentals/10-bias-variance" },
      { name: "Ensemble Methods: Boosting, Bagging, Stacking", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/11-ensemble-methods" },
      { name: "Hyperparameter Tuning", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/12-hyperparameter-tuning" },
      { name: "ML Pipelines & Experiment Tracking", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/13-ml-pipelines" },
      { name: "Naive Bayes", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/14-naive-bayes" },
      { name: "Time Series Fundamentals", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/15-time-series" },
      { name: "Anomaly Detection", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/16-anomaly-detection" },
      { name: "Handling Imbalanced Data", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/17-imbalanced-data" },
      { name: "Feature Selection", status: "complete", type: "Build", lang: "Python", path: "phases/02-ml-fundamentals/18-feature-selection" }
    ]
  },
  {
    id: 3,
    name: "Deep Learning Core",
    status: "complete",
    desc: "Neural networks from first principles. No frameworks until you build one.",
    lessons: [
      { name: "The Perceptron: Where It All Started", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/01-the-perceptron" },
      { name: "Multi-Layer Networks & Forward Pass", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/02-multi-layer-networks" },
      { name: "Backpropagation from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/03-backpropagation" },
      { name: "Activation Functions: ReLU, Sigmoid, GELU & Why", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/04-activation-functions" },
      { name: "Loss Functions: MSE, Cross-Entropy, Contrastive", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/05-loss-functions" },
      { name: "Optimizers: SGD, Momentum, Adam, AdamW", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/06-optimizers" },
      { name: "Regularization: Dropout, Weight Decay, BatchNorm", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/07-regularization" },
      { name: "Weight Initialization & Training Stability", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/08-weight-initialization" },
      { name: "Learning Rate Schedules & Warmup", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/09-learning-rate-schedules" },
      { name: "Build Your Own Mini Framework", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/10-mini-framework" },
      { name: "Introduction to PyTorch", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/11-intro-to-pytorch" },
      { name: "Introduction to JAX", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/12-intro-to-jax" },
      { name: "Debugging Neural Networks", status: "complete", type: "Build", lang: "Python", path: "phases/03-deep-learning-core/13-debugging-neural-networks" }
    ]
  },
  {
    id: 4,
    name: "Computer Vision",
    status: "complete",
    desc: "From pixels to understanding — image, video, 3D, VLMs, and world models.",
    lessons: [
      { name: "Image Fundamentals: Pixels, Channels, Color Spaces", status: "complete", type: "Learn", lang: "Python", path: "phases/04-computer-vision/01-image-fundamentals" },
      { name: "Convolutions from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/02-convolutions-from-scratch" },
      { name: "CNNs: LeNet to ResNet", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/03-cnns-lenet-to-resnet" },
      { name: "Image Classification", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/04-image-classification" },
      { name: "Transfer Learning & Fine-Tuning", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/05-transfer-learning" },
      { name: "Object Detection — YOLO from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/06-object-detection-yolo" },
      { name: "Semantic Segmentation — U-Net", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/07-semantic-segmentation-unet" },
      { name: "Instance Segmentation — Mask R-CNN", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/08-instance-segmentation-mask-rcnn" },
      { name: "Image Generation — GANs", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/09-image-generation-gans" },
      { name: "Image Generation — Diffusion Models", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/10-image-generation-diffusion" },
      { name: "Stable Diffusion — Architecture & Fine-Tuning", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/11-stable-diffusion" },
      { name: "Video Understanding — Temporal Modeling", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/12-video-understanding" },
      { name: "3D Vision: Point Clouds, NeRFs", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/13-3d-vision-nerf" },
      { name: "Vision Transformers (ViT)", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/14-vision-transformers" },
      { name: "Real-Time Vision: Edge Deployment", status: "complete", type: "Build", lang: "Python, Rust", path: "phases/04-computer-vision/15-real-time-edge" },
      { name: "Build a Complete Vision Pipeline", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/16-vision-pipeline-capstone" },
      { name: "Self-Supervised Vision — SimCLR, DINO, MAE", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/17-self-supervised-vision" },
      { name: "Open-Vocabulary Vision — CLIP", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/18-open-vocab-clip" },
      { name: "OCR & Document Understanding", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/19-ocr-document-understanding" },
      { name: "Image Retrieval & Metric Learning", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/20-image-retrieval-metric" },
      { name: "Keypoint Detection & Pose Estimation", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/21-keypoint-pose" },
      { name: "3D Gaussian Splatting from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/22-3d-gaussian-splatting" },
      { name: "Diffusion Transformers & Rectified Flow", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/23-diffusion-transformers-rectified-flow" },
      { name: "SAM 3 & Open-Vocabulary Segmentation", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/24-sam3-open-vocab-segmentation" },
      { name: "Vision-Language Models (ViT-MLP-LLM)", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/25-vision-language-models" },
      { name: "Monocular Depth & Geometry Estimation", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/26-monocular-depth" },
      { name: "Multi-Object Tracking & Video Memory", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/27-multi-object-tracking" },
      { name: "World Models & Video Diffusion", status: "complete", type: "Build", lang: "Python", path: "phases/04-computer-vision/28-world-models-video-diffusion" }
    ]
  },
  {
    id: 5,
    name: "NLP: Foundations to Advanced",
    status: "planned",
    desc: "Language is the interface to intelligence.",
    lessons: [
      { name: "Text Processing: Tokenization, Stemming, Lemmatization", status: "planned", type: "Build", lang: "Python" },
      { name: "Bag of Words, TF-IDF & Text Representation", status: "planned", type: "Build", lang: "Python" },
      { name: "Word Embeddings: Word2Vec from Scratch", status: "planned", type: "Build", lang: "Python" },
      { name: "GloVe, FastText & Subword Embeddings", status: "planned", type: "Build", lang: "Python" },
      { name: "Sentiment Analysis", status: "planned", type: "Build", lang: "Python" },
      { name: "Named Entity Recognition (NER)", status: "planned", type: "Build", lang: "Python" },
      { name: "POS Tagging & Syntactic Parsing", status: "planned", type: "Build", lang: "Python" },
      { name: "Text Classification — CNNs & RNNs for Text", status: "planned", type: "Build", lang: "Python" },
      { name: "Sequence-to-Sequence Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Attention Mechanism — The Breakthrough", status: "planned", type: "Build", lang: "Python" },
      { name: "Machine Translation", status: "planned", type: "Build", lang: "Python" },
      { name: "Text Summarization", status: "planned", type: "Build", lang: "Python" },
      { name: "Question Answering Systems", status: "planned", type: "Build", lang: "Python" },
      { name: "Information Retrieval & Search", status: "planned", type: "Build", lang: "Python" },
      { name: "Topic Modeling: LDA, BERTopic", status: "planned", type: "Build", lang: "Python" },
      { name: "Text Generation", status: "planned", type: "Build", lang: "Python" },
      { name: "Chatbots: Rule-Based to Neural", status: "planned", type: "Build", lang: "Python" },
      { name: "Multilingual NLP", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 6,
    name: "Speech & Audio",
    status: "planned",
    desc: "Hear, understand, speak.",
    lessons: [
      { name: "Audio Fundamentals: Waveforms, Sampling, FFT", status: "planned", type: "Learn", lang: "Python" },
      { name: "Spectrograms, Mel Scale & Audio Features", status: "planned", type: "Build", lang: "Python" },
      { name: "Audio Classification", status: "planned", type: "Build", lang: "Python" },
      { name: "Speech Recognition (ASR)", status: "planned", type: "Build", lang: "Python" },
      { name: "Whisper: Architecture & Fine-Tuning", status: "planned", type: "Build", lang: "Python" },
      { name: "Speaker Recognition & Verification", status: "planned", type: "Build", lang: "Python" },
      { name: "Text-to-Speech (TTS)", status: "planned", type: "Build", lang: "Python" },
      { name: "Voice Cloning & Voice Conversion", status: "planned", type: "Build", lang: "Python" },
      { name: "Music Generation", status: "planned", type: "Build", lang: "Python" },
      { name: "Audio-Language Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Real-Time Audio Processing", status: "planned", type: "Build", lang: "Python, Rust" },
      { name: "Build a Voice Assistant Pipeline", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 7,
    name: "Transformers Deep Dive",
    status: "in-progress",
    desc: "The architecture that changed everything.",
    lessons: [
      { name: "Why Transformers: The Problems with RNNs", status: "planned", type: "Learn", lang: "—" },
      { name: "Self-Attention from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/02-self-attention-from-scratch" },
      { name: "Multi-Head Attention", status: "planned", type: "Build", lang: "Python" },
      { name: "Positional Encoding: Sinusoidal, RoPE, ALiBi", status: "planned", type: "Build", lang: "Python" },
      { name: "The Full Transformer: Encoder + Decoder", status: "planned", type: "Build", lang: "Python" },
      { name: "BERT — Masked Language Modeling", status: "planned", type: "Build", lang: "Python" },
      { name: "GPT — Causal Language Modeling", status: "planned", type: "Build", lang: "Python" },
      { name: "T5, BART — Encoder-Decoder Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Vision Transformers (ViT)", status: "planned", type: "Build", lang: "Python" },
      { name: "Audio Transformers — Whisper Architecture", status: "planned", type: "Build", lang: "Python" },
      { name: "Mixture of Experts (MoE)", status: "planned", type: "Build", lang: "Python" },
      { name: "KV Cache, Flash Attention & Inference Optimization", status: "planned", type: "Build", lang: "Python, Rust" },
      { name: "Scaling Laws", status: "planned", type: "Learn", lang: "Python" },
      { name: "Build a Transformer from Scratch", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 8,
    name: "Generative AI",
    status: "planned",
    desc: "Create images, video, audio, 3D, and more.",
    lessons: [
      { name: "Generative Models: Taxonomy & History", status: "planned", type: "Learn", lang: "—" },
      { name: "Autoencoders & VAE", status: "planned", type: "Build", lang: "Python" },
      { name: "GANs: Generator vs Discriminator", status: "planned", type: "Build", lang: "Python" },
      { name: "Conditional GANs & Pix2Pix", status: "planned", type: "Build", lang: "Python" },
      { name: "StyleGAN", status: "planned", type: "Build", lang: "Python" },
      { name: "Diffusion Models — DDPM from Scratch", status: "planned", type: "Build", lang: "Python" },
      { name: "Latent Diffusion & Stable Diffusion", status: "planned", type: "Build", lang: "Python" },
      { name: "ControlNet, LoRA & Conditioning", status: "planned", type: "Build", lang: "Python" },
      { name: "Inpainting, Outpainting & Editing", status: "planned", type: "Build", lang: "Python" },
      { name: "Video Generation", status: "planned", type: "Build", lang: "Python" },
      { name: "Audio Generation", status: "planned", type: "Build", lang: "Python" },
      { name: "3D Generation", status: "planned", type: "Build", lang: "Python" },
      { name: "Flow Matching & Rectified Flows", status: "planned", type: "Build", lang: "Python" },
      { name: "Evaluation: FID, CLIP Score", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 9,
    name: "Reinforcement Learning",
    status: "planned",
    desc: "The foundation of RLHF and game-playing AI.",
    lessons: [
      { name: "MDPs, States, Actions & Rewards", status: "planned", type: "Learn", lang: "Python" },
      { name: "Dynamic Programming", status: "planned", type: "Build", lang: "Python" },
      { name: "Monte Carlo Methods", status: "planned", type: "Build", lang: "Python" },
      { name: "Q-Learning, SARSA", status: "planned", type: "Build", lang: "Python" },
      { name: "Deep Q-Networks (DQN)", status: "planned", type: "Build", lang: "Python" },
      { name: "Policy Gradients — REINFORCE", status: "planned", type: "Build", lang: "Python" },
      { name: "Actor-Critic — A2C, A3C", status: "planned", type: "Build", lang: "Python" },
      { name: "PPO", status: "planned", type: "Build", lang: "Python" },
      { name: "Reward Modeling & RLHF", status: "planned", type: "Build", lang: "Python" },
      { name: "Multi-Agent RL", status: "planned", type: "Build", lang: "Python" },
      { name: "Sim-to-Real Transfer", status: "planned", type: "Build", lang: "Python" },
      { name: "RL for Games", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 10,
    name: "LLMs from Scratch",
    status: "in-progress",
    desc: "Build, train, and understand large language models.",
    lessons: [
      { name: "Tokenizers: BPE, WordPiece, SentencePiece", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/01-tokenizers" },
      { name: "Building a Tokenizer from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/02-building-a-tokenizer" },
      { name: "Data Pipelines for Pre-Training", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/03-data-pipelines" },
      { name: "Pre-Training a Mini GPT (124M)", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/04-pre-training-mini-gpt" },
      { name: "Distributed Training, FSDP, DeepSpeed", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/05-scaling-distributed" },
      { name: "Instruction Tuning — SFT", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/06-instruction-tuning-sft" },
      { name: "RLHF — Reward Model + PPO", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/07-rlhf" },
      { name: "DPO — Direct Preference Optimization", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/08-dpo" },
      { name: "Constitutional AI", status: "planned", type: "Build", lang: "Python" },
      { name: "Evaluation — Benchmarks, Evals", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/10-evaluation" },
      { name: "Quantization: INT8, GPTQ, AWQ, GGUF", status: "complete", type: "Build", lang: "Python, Rust" },
      { name: "Inference Optimization", status: "complete", type: "Build", lang: "Python" },
      { name: "Building a Complete LLM Pipeline", status: "planned", type: "Build", lang: "Python" },
      { name: "Open Models: Architecture Walkthroughs", status: "planned", type: "Learn", lang: "Python" }
    ]
  },
  {
    id: 11,
    name: "LLM Engineering",
    status: "complete",
    desc: "Put LLMs to work in production.",
    lessons: [
      { name: "Prompt Engineering: Techniques & Patterns", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/01-prompt-engineering" },
      { name: "Few-Shot, CoT, Tree-of-Thought", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/02-few-shot-cot" },
      { name: "Structured Outputs", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/03-structured-outputs" },
      { name: "Embeddings & Vector Representations", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/04-embeddings" },
      { name: "Context Engineering", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/05-context-engineering" },
      { name: "RAG: Retrieval-Augmented Generation", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/06-rag" },
      { name: "Advanced RAG: Chunking, Reranking", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/07-advanced-rag" },
      { name: "Fine-Tuning with LoRA & QLoRA", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/08-fine-tuning-lora" },
      { name: "Function Calling & Tool Use", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/09-function-calling" },
      { name: "Evaluation & Testing", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/10-evaluation" },
      { name: "Caching, Rate Limiting & Cost", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/11-caching-cost" },
      { name: "Guardrails & Safety", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/12-guardrails" },
      { name: "Building a Production LLM App", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/13-production-app" }
    ]
  },
  {
    id: 12,
    name: "Multimodal AI",
    status: "planned",
    desc: "See, hear, read, and reason across modalities.",
    lessons: [
      { name: "Multimodal Representations", status: "planned", type: "Learn", lang: "—" },
      { name: "CLIP: Vision + Language", status: "planned", type: "Build", lang: "Python" },
      { name: "Vision-Language Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Audio-Language Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Document Understanding", status: "planned", type: "Build", lang: "Python" },
      { name: "Video-Language Models", status: "planned", type: "Build", lang: "Python" },
      { name: "Multimodal RAG", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Multimodal Agents", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Text-to-Image Pipelines", status: "planned", type: "Build", lang: "Python" },
      { name: "Text-to-Video Pipelines", status: "planned", type: "Build", lang: "Python" },
      { name: "Any-to-Any Models", status: "planned", type: "Learn", lang: "Python" }
    ]
  },
  {
    id: 13,
    name: "Tools & Protocols",
    status: "planned",
    desc: "The interfaces between AI and the real world.",
    lessons: [
      { name: "Function Calling Deep Dive", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Tool Use Patterns", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "MCP: Model Context Protocol", status: "planned", type: "Learn", lang: "—" },
      { name: "Building MCP Servers", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "Building MCP Clients", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "MCP Resources, Prompts & Sampling", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Structured Output Schemas", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "API Design for AI", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Browser Automation & Web Agents", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Build a Complete Tool Ecosystem", status: "planned", type: "Build", lang: "TypeScript, Python" }
    ]
  },
  {
    id: 14,
    name: "Agent Engineering",
    status: "in-progress",
    desc: "Build agents from first principles.",
    lessons: [
      { name: "The Agent Loop", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/14-agent-engineering/01-the-agent-loop" },
      { name: "Tool Dispatch & Registration", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Planning: TodoWrite, DAGs", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Memory: Short-Term, Long-Term, Episodic", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "Context Window Management", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Context Compression & Summarization", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Subagents: Delegation", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Skills & Knowledge Loading", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Permissions, Sandboxing & Safety", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "File-Based Task Systems", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Background Task Execution", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Error Recovery & Self-Healing", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Hooks: PreToolUse, PostToolUse", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Eval-Driven Agent Development", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Build a Complete AI Agent", status: "planned", type: "Build", lang: "TypeScript" }
    ]
  },
  {
    id: 15,
    name: "Autonomous Systems",
    status: "planned",
    desc: "Agents that run without human intervention safely.",
    lessons: [
      { name: "What Makes a System Autonomous", status: "planned", type: "Learn", lang: "—" },
      { name: "Autonomous Loops", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "Self-Healing Agents", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "AutoResearch: Autonomous Research", status: "planned", type: "Build", lang: "TypeScript, Python" },
      { name: "Eval-Driven Loops", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Human-in-the-Loop", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Continuous Agents", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Cost-Aware Autonomous Systems", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Monitoring & Observability", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "Safety Boundaries", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Build an Autonomous Coding Agent", status: "planned", type: "Build", lang: "TypeScript" }
    ]
  },
  {
    id: 16,
    name: "Multi-Agent & Swarms",
    status: "in-progress",
    desc: "Coordination, emergence, and collective intelligence.",
    lessons: [
      { name: "Why Multi-Agent", status: "complete", type: "Learn", lang: "—", path: "phases/16-multi-agent-and-swarms/01-why-multi-agent" },
      { name: "Agent Teams: Roles & Delegation", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Communication Protocols", status: "complete", type: "Build", lang: "TypeScript", path: "phases/16-multi-agent-and-swarms/03-communication-protocols" },
      { name: "Shared State & Coordination", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "Message Passing & Mailboxes", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Task Markets", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Consensus Algorithms", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "Swarm Intelligence", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Agent Economies", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Worktree Isolation", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Hierarchical Swarms", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "Self-Organizing Systems", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "DAG-Based Orchestration", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "Build an Autonomous Swarm", status: "planned", type: "Build", lang: "TypeScript, Rust" }
    ]
  },
  {
    id: 17,
    name: "Infrastructure & Production",
    status: "in-progress",
    desc: "Ship AI to the real world.",
    lessons: [
      { name: "Model Serving", status: "complete", type: "Build", lang: "Python" },
      { name: "Docker for AI Workloads", status: "complete", type: "Build", lang: "Python, Rust" },
      { name: "Kubernetes for AI", status: "complete", type: "Build", lang: "Python" },
      { name: "Edge Deployment: ONNX, WASM", status: "planned", type: "Build", lang: "Python, Rust" },
      { name: "Observability", status: "planned", type: "Build", lang: "TypeScript, Rust" },
      { name: "Cost Optimization", status: "planned", type: "Build", lang: "TypeScript" },
      { name: "CI/CD for ML", status: "planned", type: "Build", lang: "Python" },
      { name: "A/B Testing & Feature Flags", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Data Pipelines", status: "planned", type: "Build", lang: "Python, Rust" },
      { name: "Security: Red Teaming, Defense", status: "planned", type: "Build", lang: "Python, TypeScript" },
      { name: "Build a Production AI Platform", status: "planned", type: "Build", lang: "Python, TypeScript, Rust" }
    ]
  },
  {
    id: 18,
    name: "Ethics, Safety & Alignment",
    status: "planned",
    desc: "Build AI that helps humanity. Not optional.",
    lessons: [
      { name: "AI Ethics: Bias, Fairness", status: "planned", type: "Learn", lang: "—" },
      { name: "Alignment: What & Why", status: "planned", type: "Learn", lang: "—" },
      { name: "Red Teaming & Adversarial Testing", status: "planned", type: "Build", lang: "Python" },
      { name: "Responsible AI Frameworks", status: "planned", type: "Learn", lang: "—" },
      { name: "Privacy: Differential Privacy, FL", status: "planned", type: "Build", lang: "Python" },
      { name: "Interpretability: SHAP, Attention", status: "planned", type: "Build", lang: "Python" }
    ]
  },
  {
    id: 19,
    name: "Capstone Projects",
    status: "planned",
    desc: "Prove everything you learned.",
    lessons: [
      { name: "🤖 Build a Mini GPT & Chat Interface", status: "planned", type: "Phases 1, 3, 7, 10", lang: "Python, TypeScript" },
      { name: "🔍 Build a Multimodal RAG System", status: "planned", type: "Phases 5, 11, 12, 13", lang: "Python, TypeScript" },
      { name: "🧪 Build an Autonomous Research Agent", status: "planned", type: "Phases 14, 15, 6", lang: "TypeScript, Python" },
      { name: "👥 Build a Multi-Agent Dev Team", status: "planned", type: "Phases 14, 15, 16, 17", lang: "TypeScript, Rust" },
      { name: "🚀 Build a Production AI Platform", status: "planned", type: "All phases", lang: "Python, TypeScript, Rust" }
    ]
  }
];

// Helper functions
export function getTotalLessons(): number {
  return PHASES.reduce((acc, phase) => acc + phase.lessons.length, 0);
}

export function getTotalPhases(): number {
  return PHASES.length;
}

export function getCompletedLessons(): number {
  return PHASES.reduce((acc, phase) => {
    return acc + phase.lessons.filter(l => l.status === 'complete').length;
  }, 0);
}

export function getLanguages(): string[] {
  return ['Python', 'TypeScript', 'Rust', 'Julia'];
}
