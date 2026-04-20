// Felix Learning Platform - Core curriculum data structure
// Built with AI-first methodology: Learn, Build, Ship

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
    status: "complete",
    desc: "Language is the interface to intelligence.",
    lessons: [
      { name: "Text Processing: Tokenization, Stemming, Lemmatization", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/01-text-processing" },
      { name: "Bag of Words, TF-IDF & Text Representation", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/02-bag-of-words-tfidf" },
      { name: "Word Embeddings: Word2Vec from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/03-word-embeddings-word2vec" },
      { name: "GloVe, FastText & Subword Embeddings", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/04-glove-fasttext-subword" },
      { name: "Sentiment Analysis", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/05-sentiment-analysis" },
      { name: "Named Entity Recognition (NER)", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/06-named-entity-recognition" },
      { name: "POS Tagging & Syntactic Parsing", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/07-pos-tagging-parsing" },
      { name: "Text Classification — CNNs & RNNs for Text", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/08-cnns-rnns-for-text" },
      { name: "Sequence-to-Sequence Models", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/09-sequence-to-sequence" },
      { name: "Attention Mechanism — The Breakthrough", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/10-attention-mechanism" },
      { name: "Machine Translation", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/11-machine-translation" },
      { name: "Text Summarization", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/12-text-summarization" },
      { name: "Question Answering Systems", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/13-question-answering" },
      { name: "Information Retrieval & Search", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/14-information-retrieval-search" },
      { name: "Topic Modeling: LDA, BERTopic", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/15-topic-modeling" },
      { name: "Text Generation (Pre-Transformer)", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/16-text-generation-pre-transformer" },
      { name: "Chatbots: Rule-Based to Neural", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/17-chatbots-rule-to-neural" },
      { name: "Multilingual NLP", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/18-multilingual-nlp" },
      { name: "Subword Tokenization", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/19-subword-tokenization" },
      { name: "Structured Outputs & Constrained Decoding", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/20-structured-outputs-constrained-decoding" },
      { name: "NLI & Textual Entailment", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/21-nli-textual-entailment" },
      { name: "Embedding Models Deep Dive", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/22-embedding-models-deep-dive" },
      { name: "Chunking Strategies for RAG", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/23-chunking-strategies-rag" },
      { name: "Coreference Resolution", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/24-coreference-resolution" },
      { name: "Entity Linking", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/25-entity-linking" },
      { name: "Relation Extraction & Knowledge Graphs", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/26-relation-extraction-kg" },
      { name: "LLM Evaluation Frameworks", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/27-llm-evaluation-frameworks" },
      { name: "Long Context Evaluation", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/28-long-context-evaluation" },
      { name: "Dialogue State Tracking", status: "complete", type: "Build", lang: "Python", path: "phases/05-nlp-foundations-to-advanced/29-dialogue-state-tracking" }
    ]
  },
  {
    id: 6,
    name: "Speech & Audio",
    status: "complete",
    desc: "Hear, understand, speak.",
    lessons: [
      { name: "Audio Fundamentals: Waveforms, Sampling, FFT", status: "complete", type: "Learn", lang: "Python", path: "phases/06-speech-and-audio/01-audio-fundamentals" },
      { name: "Spectrograms, Mel Scale & Audio Features", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/02-spectrograms-mel-features" },
      { name: "Audio Classification", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/03-audio-classification" },
      { name: "Speech Recognition (ASR)", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/04-speech-recognition-asr" },
      { name: "Whisper: Architecture & Fine-Tuning", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/05-whisper-architecture-finetuning" },
      { name: "Speaker Recognition & Verification", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/06-speaker-recognition-verification" },
      { name: "Text-to-Speech (TTS)", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/07-text-to-speech" },
      { name: "Voice Cloning & Voice Conversion", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/08-voice-cloning-conversion" },
      { name: "Music Generation", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/09-music-generation" },
      { name: "Audio-Language Models", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/10-audio-language-models" },
      { name: "Real-Time Audio Processing", status: "complete", type: "Build", lang: "Python, Rust", path: "phases/06-speech-and-audio/11-real-time-audio-processing" },
      { name: "Build a Voice Assistant Pipeline", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/12-voice-assistant-pipeline" },
      { name: "Neural Audio Codecs", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/13-neural-audio-codecs" },
      { name: "Voice Activity Detection & Turn-Taking", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/14-voice-activity-detection-turn-taking" },
      { name: "Streaming Speech-to-Speech: Moshi & Hibiki", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/15-streaming-speech-to-speech-moshi-hibiki" },
      { name: "Anti-Spoofing & Audio Watermarking", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/16-anti-spoofing-audio-watermarking" },
      { name: "Audio Evaluation Metrics", status: "complete", type: "Build", lang: "Python", path: "phases/06-speech-and-audio/17-audio-evaluation-metrics" }
    ]
  },
  {
    id: 7,
    name: "Transformers Deep Dive",
    status: "complete",
    desc: "The architecture that changed everything.",
    lessons: [
      { name: "Why Transformers: The Problems with RNNs", status: "complete", type: "Learn", lang: "—", path: "phases/07-transformers-deep-dive/01-why-transformers" },
      { name: "Self-Attention from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/02-self-attention-from-scratch" },
      { name: "Multi-Head Attention", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/03-multi-head-attention" },
      { name: "Positional Encoding: Sinusoidal, RoPE, ALiBi", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/04-positional-encoding" },
      { name: "The Full Transformer: Encoder + Decoder", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/05-full-transformer" },
      { name: "BERT — Masked Language Modeling", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/06-bert-masked-language-modeling" },
      { name: "GPT — Causal Language Modeling", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/07-gpt-causal-language-modeling" },
      { name: "T5, BART — Encoder-Decoder Models", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/08-t5-bart-encoder-decoder" },
      { name: "Vision Transformers (ViT)", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/09-vision-transformers" },
      { name: "Audio Transformers — Whisper Architecture", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/10-audio-transformers-whisper" },
      { name: "Mixture of Experts (MoE)", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/11-mixture-of-experts" },
      { name: "KV Cache, Flash Attention & Inference Optimization", status: "complete", type: "Build", lang: "Python, Rust", path: "phases/07-transformers-deep-dive/12-kv-cache-flash-attention" },
      { name: "Scaling Laws", status: "complete", type: "Learn", lang: "Python", path: "phases/07-transformers-deep-dive/13-scaling-laws" },
      { name: "Build a Transformer from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/14-build-a-transformer-capstone" },
      { name: "Attention Variants", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/15-attention-variants" },
      { name: "Speculative Decoding", status: "complete", type: "Build", lang: "Python", path: "phases/07-transformers-deep-dive/16-speculative-decoding" }
    ]
  },
  {
    id: 8,
    name: "Generative AI",
    status: "complete",
    desc: "Create images, video, audio, 3D, and more.",
    lessons: [
      { name: "Generative Models: Taxonomy & History", status: "complete", type: "Learn", lang: "—", path: "phases/08-generative-ai/01-generative-models-taxonomy-history" },
      { name: "Autoencoders & VAE", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/02-autoencoders-vae" },
      { name: "GANs: Generator vs Discriminator", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/03-gans-generator-discriminator" },
      { name: "Conditional GANs & Pix2Pix", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/04-conditional-gans-pix2pix" },
      { name: "StyleGAN", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/05-stylegan" },
      { name: "Diffusion Models — DDPM from Scratch", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/06-diffusion-ddpm-from-scratch" },
      { name: "Latent Diffusion & Stable Diffusion", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/07-latent-diffusion-stable-diffusion" },
      { name: "ControlNet, LoRA & Conditioning", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/08-controlnet-lora-conditioning" },
      { name: "Inpainting, Outpainting & Editing", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/09-inpainting-outpainting-editing" },
      { name: "Video Generation", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/10-video-generation" },
      { name: "Audio Generation", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/11-audio-generation" },
      { name: "3D Generation", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/12-3d-generation" },
      { name: "Flow Matching & Rectified Flows", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/13-flow-matching-rectified-flows" },
      { name: "Evaluation: FID, CLIP Score", status: "complete", type: "Build", lang: "Python", path: "phases/08-generative-ai/14-evaluation-fid-clip-score" }
    ]
  },
  {
    id: 9,
    name: "Reinforcement Learning",
    status: "complete",
    desc: "The foundation of RLHF and game-playing AI.",
    lessons: [
      { name: "MDPs, States, Actions & Rewards", status: "complete", type: "Learn", lang: "Python", path: "phases/09-reinforcement-learning/01-mdps-states-actions-rewards" },
      { name: "Dynamic Programming", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/02-dynamic-programming" },
      { name: "Monte Carlo Methods", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/03-monte-carlo-methods" },
      { name: "Q-Learning, SARSA", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/04-q-learning-sarsa" },
      { name: "Deep Q-Networks (DQN)", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/05-dqn" },
      { name: "Policy Gradients — REINFORCE", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/06-policy-gradients-reinforce" },
      { name: "Actor-Critic — A2C, A3C", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/07-actor-critic-a2c-a3c" },
      { name: "PPO", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/08-ppo" },
      { name: "Reward Modeling & RLHF", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/09-reward-modeling-rlhf" },
      { name: "Multi-Agent RL", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/10-multi-agent-rl" },
      { name: "Sim-to-Real Transfer", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/11-sim-to-real-transfer" },
      { name: "RL for Games", status: "complete", type: "Build", lang: "Python", path: "phases/09-reinforcement-learning/12-rl-for-games" }
    ]
  },
  {
    id: 10,
    name: "LLMs from Scratch",
    status: "complete",
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
      { name: "Constitutional AI & Self-Improvement", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/09-constitutional-ai-self-improvement" },
      { name: "Evaluation — Benchmarks, Evals", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/10-evaluation" },
      { name: "Quantization: INT8, GPTQ, AWQ, GGUF", status: "complete", type: "Build", lang: "Python, Rust", path: "phases/10-llms-from-scratch/11-quantization" },
      { name: "Inference Optimization", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/12-inference-optimization" },
      { name: "Building a Complete LLM Pipeline", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/13-building-complete-llm-pipeline" },
      { name: "Open Models: Architecture Walkthroughs", status: "complete", type: "Learn", lang: "Python", path: "phases/10-llms-from-scratch/14-open-models-architecture-walkthroughs" },
      { name: "Speculative Decoding: Eagle 3", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/15-speculative-decoding-eagle3" },
      { name: "Differential Attention V2", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/16-differential-attention-v2" },
      { name: "Native Sparse Attention", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/17-native-sparse-attention" },
      { name: "Multi-Token Prediction", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/18-multi-token-prediction" },
      { name: "DualPipe Parallelism", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/19-dualpipe-parallelism" },
      { name: "DeepSeek-V3 Walkthrough", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/20-deepseek-v3-walkthrough" },
      { name: "Jamba: Hybrid SSM-Transformer", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/21-jamba-hybrid-ssm-transformer" },
      { name: "Async Hogwild Inference", status: "complete", type: "Build", lang: "Python", path: "phases/10-llms-from-scratch/22-async-hogwild-inference" }
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
      { name: "Building a Production LLM App", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/13-production-app" },
      { name: "Model Context Protocol (MCP)", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/14-model-context-protocol" },
      { name: "Prompt Caching", status: "complete", type: "Build", lang: "Python", path: "phases/11-llm-engineering/15-prompt-caching" },
      { name: "LangGraph State Machines", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/16-langgraph-state-machines" },
      { name: "Agent Framework Tradeoffs", status: "complete", type: "Build", lang: "Python, TypeScript", path: "phases/11-llm-engineering/17-agent-framework-tradeoffs" }
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
    status: "complete",
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
    status: "complete",
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
    status: "complete",
    desc: "Ship AI to the real world.",
    lessons: [
      { name: "Model Serving", status: "complete", type: "Build", lang: "Python", path: "phases/17-infrastructure-and-production/01-model-serving" },
      { name: "Docker for AI Workloads", status: "complete", type: "Build", lang: "Python, Rust", path: "phases/17-infrastructure-and-production/02-docker-for-ai" },
      { name: "Kubernetes for AI", status: "complete", type: "Build", lang: "Python", path: "phases/17-infrastructure-and-production/03-kubernetes-for-ai" },
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
