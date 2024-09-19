![The banner reproducing a technological skyline of a futuristic business district governed by Artificial Intelligence](./images/pb67-Banner.png)

# Enanching RAG systems with HAP language filtering

The integration of a Hate, Abuse, and Profanity (HAP) language filters within Retrieval-Augmented Generation (RAG) systems is critical for ensuring the ethical and responsible use of large language models (LLMs).
Indeed, Large Language Models (LLMs) are central to many modern Natural Language Processing (NLP) tasks, but their reliance on vast amounts of data from the web poses a significant risk of generating harmful content. As highlighted by Christoph Tillmann and colleagues (reference), LLMs, including widely-used models like RoBERTa, can inadvertently produce hate, abuse, and profanity (HAP) content due to being trained on datasets that may contain offensive material​. In this context, the authors suggest different approaches to avoid such behaviors focusing on HAP filtering during models' training and alignment, in order to assure that an LLM does not rely on such language when producing content; furthermore, they also provide indication on how to deal with HAP filtering 
However, considering Retrieval-Augmented Generation (RAG) systems, where LLMs generate responses based on large document repositories, the risk of producing HAP content in response to a user query can also emerge from the presence of HAP language in the RAG system's knowledge base.

Hence, when it comes to filtering HAP content in the context of a RAG system, we can identify two primary approaches:

- Filtering the documents that are ingested into the RAG system, ensuring the knowledge base remains free of HAP language (pre-processing approach).
- Filtering the model’s output to sanitize responses, reducing the risk of harmful content being generated (post-processing approach).

Each method has its own benefits and challenges. Filtering documents during ingestion ensures that harmful content is never introduced into the knowledge base, preventing the possibility of such content being retrieved or surfaced in the model’s output. On the other hand, filtering the output of the LLM can be useful in cases where harmful language is inadvertently generated or inferred based on user queries, but this approach does not preclude the system from retrieving or working with problematic content behind the scenes.

However, most existing HAP filters focus on removing harmful content entirely, which poses its own challenges. By stripping away HAP content, valuable information or context, which may be crucial in sensitive domains such as law enforcement or social work, could be lost. For instance, an important document discussing hate speech could be discarded entirely, despite having substantial insights.

In this article, we will show how to easily implement a pipeline that identifies HAP language within documents intended for ingestion (pre-processing approach) and, rather than discarding these sections, pass the flagged content to an LLM, which will rephrase the HAP elements into a more appropriate form while preserving the original meaning and context. The cleaned documents can then be ingested into the RAG system, ensuring both the integrity of the knowledge base and the ethical use of language. This approach not only safeguards the user experience but also maximizes the amount of usable, meaningful content available to the system. Furthermore, in order to assure that users' queries will not force the LLM to produce HAP content, we will introduce a post-processing filter aimed to detect HAP language in the generated content and rephrase it if needed.

In doing so, we expand our preavious work on how to build a RAG system (reference) leveraging IBM Granite Guardium, a highly effective classifier for identifying hate, abuse, and profanity (HAP) content recently open-sourced by IBM Research (reference), for classifing HAP content within the knowledge base. Trained on large-scale datasets, IBM Granite Guardium boasts a lightweight model with only 38 million parameters, allowing it to deliver accurate HAP detection for the english language with lower computational requirements. Its streamlined performance ensures quick and reliable identification of harmful content, making it an ideal tool for real-time applications in content moderation, while maintaining the scalability needed for large RAG systems. Finally, we will show how to easily identify HAP content in the output of models hosted in IBM watsonx's foundational model library by leveraging the "AI Guardrails" feature embedded in IBM watsonx.

# Identify HAP content in the knowledge base using IBM Granite Guardium

Differently from our preavious work, we introduce a new pre-processing step aimed at identifying documents containing HAP content. In order to do so, we split our documents into chuncks of text that we will pass to our HAP classifier. 

(fig1)

Then we need load the IBM Granite Guardian 38M model, which can be easily pulled from its HuggingFace Repository. The model take string of text as input and compute the probability that the processed text may contain HAP language: in its basic settings, if the probability associated to a string is higher than 0.5, the string is classified as 1 (indicating that it may contain HAP language), otherwise it is classified as 0 (i.e. no HAP content detected). For the sake of our analysis, we decide to select only the chuncks of text presenting a probability higher than 0.9 but the code can be easily adapted in order to select the preferred treshold for the specific use case.

(fig2)

Once we have identified the chunck on documents containing HAP language, we can build a dictionary containing all the documents containing such chuncks for later processing.

(fig3)

Now we need to build-up a few functions for manipulating the documents containing the chuncks we want to transform, in particular we will need to identify these chuncks, extract it from the documents and rebuild the documents once the selected chuncks are processed and trasformed in order to remove the HAP content.

(fig4)

# Rephrasing HAP content within documents while maintaining information

We are now ready to process the HAP content in order to transform it so to maintain as much information as possible while rephrasing the text in proper language. In doing so, we leverage the foundational models available in IBM watsonx.ai: this will help us in selecting the model the best fit our requisites, since we can easily analize the model cards containing relevant information on model training, performance and cost. In particular, since we are willing to ensure that our RAG workflow avoid to produce any HAP content, we select IBM Granite 13B Instruct due to the data filtering process adopted at training time (which ensure limited possible exposure to HAP content during model training) and its balanced performace/cost ratio.




# HAP filtering LLMs'output using IBM watsonx's AI Guardrails feature
