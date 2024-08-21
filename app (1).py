#!/usr/bin/env python

from __future__ import annotations

import gradio as gr

from model_list import ModelList

DESCRIPTION = '# Explore Biology & Biochemistry Foundation Models 🧬'
NOTES = '''
Thanks to the following folks who have made suggestions to this list!
- [Shelby](https://twitter.com/shelbynewsad), author of [this nice model list](https://compoundvc.notion.site/compoundvc/474885e638e94e44a1aab4d3124e3d6a?v=299bce7af785413da4c9f36837c03aaf) 
- [Valentyn Bezshapkin](https://twitter.com/valentynbez)
- [Payel Das](https://twitter.com/payel791)
- [Anthony Costa](https://twitter.com/anthonycosta)
'''
FOOTER = ''''''

def main():
    model_list = ModelList()

    with gr.Blocks(css='style.css') as demo:
        gr.Markdown(DESCRIPTION)

        search_box = gr.Textbox(
            label='Search Model Name',
            placeholder=
            'You can search for titles with regular expressions. e.g. (?<!sur)face',
            max_lines=1)
        
        case_sensitive = gr.Checkbox(label='Case Sensitive')
        
        filter_names = gr.CheckboxGroup(choices=[
            'Paper',
            'Code',
            'Model Weights',
        ], label='Filter')

        data_type_names = [
            'DNA', 'scRNA', 'mRNA', 'scRNA perturbation', 'RNA structure prediction', 'RNA language model', 'protein language model', 'protein structure prediction', 
            'protein generation', 'protein function prediction', 'protein fitness prediction', 'antibody structure prediction', 'antibody language model', 'molecules',
            'ligand generation', 'reaction-to-enzyme', 'enzyme generation', 'epigenomic', 'molecular docking', 'peptide property prediction', 
        ]

        data_types = gr.CheckboxGroup(choices=data_type_names,
                                      value=data_type_names,
                                      label='Type')

        years = ['2020', '2021', '2022', '2023']

        years_checkbox = gr.CheckboxGroup(choices=years, value=years, label='Year of Publication/Preprint')

        # model_type_names = [
        #     'GPT2', 'GPT-Neo', 'GPT-NeoX', 'ESM', 'BERT', 'RoBERTa', 'BART', 'T5', 'MPNN', 'diffusion', 'custom model'
        # ]

        # model_types = gr.CheckboxGroup(choices=model_type_names,
        #                                value=model_type_names,
        #                                label='Base Model')
        
        search_button = gr.Button('Search')

        number_of_models = gr.Textbox(label='Number of Models Found')
        table = gr.HTML(show_label=False)

        gr.Markdown(NOTES)
        gr.Markdown(FOOTER)

        demo.load(fn=model_list.render,
                  inputs=[
                      search_box,
                      case_sensitive,
                      filter_names,
                      data_types,
                      years_checkbox,
                      #model_types
                  ],
                  outputs=[
                      number_of_models,
                      table,
                  ])
        search_box.submit(fn=model_list.render,
                          inputs=[
                              search_box,
                              case_sensitive,
                              filter_names,
                              data_types,
                              years_checkbox,
                              #model_types
                          ],
                          outputs=[
                              number_of_models,
                              table,
                          ])

        search_button.click(fn=model_list.render,
                            inputs=[
                                search_box,
                                case_sensitive,
                                filter_names,
                                data_types,
                                years_checkbox,
                                #model_types
                            ],
                            outputs=[
                                number_of_models,
                                table,
                            ])

    demo.launch(enable_queue=True, share=False)


if __name__ == '__main__':
    main()
