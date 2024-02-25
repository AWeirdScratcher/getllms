<div align="center">

<img
  src="https://github.com/AWeirdScratcher/getllms/assets/90096971/3280e416-2e9a-4ae5-965d-c1c69d351d90"
  alt="Unplash / Sean Sinclair"
  />

# getllms - 1.2

The LLMs index. Uses the [LMStudio Catalog](https://github.com/lmstudio-ai/model-catalog).

`$ pip install getllms`

</div>

<br />

<details>
  <summary>
    <table>
      <thead>
        <tr>
          <th>In This Version</th>
        </tr>
      </thead>
    </table>
  </summary>
  <p>

**What's New**

- `0.5`: Support for Notebooks
- `0.4`: Minor fixes
- `1.1`: Download updates
- `1.2`: Added CLI

  </p>
</details>

## List All LLMs.

List all LLMs available for use. Selected for you.

```python
import getllms

models = getllms.list_models()
```

<details>
    <summary>Output</summary>
<p>

```python
[
  Model(
    name="Google's Gemma 2B Instruct", 
    description='** Requires LM Studio 0.2.15 or new…', 
    files=[ …(1) ]
  ), 
  Model(
    name='Mistral 7B Instruct v0.2', 
    description='The Mistral-7B-Instruct-v0.2 Large …', 
    files=[ …(2) ]
  ),
  ...
]
```

</p>
</details>

<br />

## See Trained LLMs.

Get the trained ones for a specific model. Select the one that meets your system requirements.

```python
# select Google's Gemma 2B Instruct
model = models[0]
model.files
```

<details>
    <summary>Output & More</summary>
<p>

**Output**

```python
FileCollection(
  best=ModelFile(
    name='gemma-2b-it-q8_0.gguf', 
    size=2669351840, 
    url='https://huggingface.co/lmstudi…'
  ),
  +0
)
```

***

**More**

Additionally, you can see all the available model files:

```python
model.files.all # [ ModelFile(...), ... ]
```

</p>
</details>

<br />

## Download LLMs.

Download the LLM that's right for you.

```python
model.download("model.bin")
```

<details>
    <summary>Output</summary>
<p>

```python
  0.0% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 900.0KB / 2.5GB (8.7MB/s)
```

</p>
</details>

***

<div align="center">

<img src="https://github.com/AWeirdScratcher/getllms/assets/90096971/42c9b72e-cd0c-4a88-85f9-dc0dd06ae7a2" alt="Unsplash / Milad Fakurian" />

# CLI

Learn how to use the CLI from the help command or refer to this page.

```bash
$ getllms
```

</div>

## List Models.

To list all models, use the `getllms list` command. Note that this truncates down to showing only 5 models. If you wish to list all of them, use `getllms list all` instead.

```bash
$ getllms list
```

<details>
    <summary>Output</summary>
<p>

```fix
Google's Gemma 2B Instruct

** Requires LM Studio 0.2.15 or newer ** Gemma is a family of lightweight LLMs built from the same research and technology Google used to create the Gemini models. Gemma models are available in two sizes, 2 billion and 7 billion parameters. These models are trained on up to 6T tokens of primarily English web documents, mathematics, and code, using a transformer architecture with enhancements like Multi-Query Attention, RoPE Embeddings, GeGLU Activations, and advanced normalization techniques.


Mistral 7B Instruct v0.2

The Mistral-7B-Instruct-v0.2 Large Language Model (LLM) is an improved instruct fine-tuned version of Mistral-7B-Instruct-v0.1. For full details of this model read MistralAI's blog post and paper.

(...)
```

</p>
</details>

<br />

## Download Models.

To download a model, use `getllms <model name>`:

```python
$ getllms "Google's Gemma 2B Instruct"
```

<details>
    <summary>Specify model size</summary>
<p>

If you wish to specify the model's size (economical/best), just add the desired size inside of square brackets after the name of the model.

```python
$ getllms "Google's Gemma 2B Instruct [economical]"
```

</p>
</details>

<br />

***

<div align="center">

© 2023 AWeirdDev. Catalog by [LMStudio](https://github.com/lmstudio-ai)

</div>
