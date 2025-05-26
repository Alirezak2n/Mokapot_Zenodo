import pandas as pd
import logging
import numpy as np


def protein_checker(protein, divider=';'):
    if divider in protein:
        pros = []
        for key in protein.split(divider):
            if 'ENTRAPMENT' in key:
                pros.append('Entrapment')
            elif 'CON' in key:
                pros.append('Contaminant')
            else:
                pros.append('HUMAN')
        pros = list(set(pros))
        if len(pros) == 1:
            return pros.pop()
        else:
            return sorted(pros)

    else:
        if 'ENTRAPMENT' in protein:
            return 'Entrapment'
        elif 'CON' in protein:
            return 'Contaminant'
        else:
            return 'HUMAN'
def protein_encoder(protein):
    encod = []
    if not isinstance(protein, list):
        protein = [protein]
    for prot in protein:
        if prot == "HUMAN":
            encod.append('1')
        elif prot == "Contaminant":
            encod.append('3')
        elif prot == "Entrapment":
            encod.append('2')
    encod = list(set(encod))
    return ('').join(sorted(encod))

def qvalue_computing(psms_table, score_column, decoy_column, decoy_label):
    if not isinstance(psms_table, pd.DataFrame):
        psms_table = pd.read_table(psms_table)
    psms_table['target'] = np.where(psms_table[decoy_column]!=decoy_label,1,0)
    psms_table['decoy'] = np.where(psms_table[decoy_column]==decoy_label,1,0)
    psms_table[score_column] = pd.to_numeric(psms_table[score_column])
    psms_table.sort_values([score_column],ascending=False,inplace=True)
    psms_table['target_cum'] = psms_table['target'].cumsum()
    psms_table['decoy_cum']=psms_table['decoy'].cumsum()
    psms_table['mokapot q-value']=psms_table['decoy_cum']/(psms_table['target_cum']+psms_table['decoy_cum'])
    psms_table.sort_values(['mokapot q-value'],inplace=True)
    psms_table.reset_index(drop=True,inplace=True)

    return psms_table

def id_counter(psms_table):
    if not isinstance(psms_table, pd.DataFrame):
        psms_table = pd.read_table(psms_table)
    length_1fdr = len(psms_table[psms_table['mokapot q-value']<=0.01])
    q_value_serie=psms_table['mokapot q-value']
    psms_index=psms_table.index
    return q_value_serie, psms_index, length_1fdr

def main(psms_table=None, fdr=0.01, divider=';'):
    """
    :param psms_table: input table, if not given it load an example table
    :param fdr: Default value is 0.01 that shows the limit we want for identification
    :param divider: You can choose between '\t', ';' or any other divider
    :return: (percentage of entrapments to human, protein categories values, output table with added columns)
    """
    if psms_table is None:
        psms_table = pd.read_table("./mokapot_default.mokapot.psms.txt")
    elif not isinstance(psms_table, pd.DataFrame):
        psms_table = pd.read_table(psms_table)
    psms_table = psms_table[psms_table['mokapot q-value'] <= fdr]
    psms_table['Protein_type'] = psms_table.apply(lambda x: protein_checker(x.Proteins, divider), axis=1)
    psms_table['Protein_encod'] = psms_table.apply(lambda x: protein_encoder(x.Protein_type), axis=1)
    entraps_Human = len(psms_table[psms_table['Protein_encod'] == '2']) / len(
        psms_table[psms_table['Protein_encod'] == '1']) * 100
    values = psms_table['Protein_encod'].value_counts().to_dict()
    # print("1=Human, 2=Entrapment, 3=Contaminant \n ", values)
    # print(f'Entrapment ratio to Human is: {entraps_Human: .5f}%')

    return entraps_Human, values, psms_table


if __name__ == '__main__':
    main()
