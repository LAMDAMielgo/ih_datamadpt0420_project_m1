import re
from p_acquisition import m_acquisition as m_ac

#-------------------------------------------------------------------------------- cleaning and saving tables

def acquire_career_info(df_career_info):
    """Career info is list_of_dfs[0]"""
    try:
        print(f'\n\n· Cleaning df_career_info ....')
        # Binarizing data
        df_career_info['dem_full_time_job'] = m_ac.yes_no_to_bool(df_career_info['dem_full_time_job'])

        # Changing nulls by unknown (qualitative params [low, medium, high, unknown])
        df_career_info['dem_education_level'] = m_ac.null_to_unknown(df_career_info['dem_education_level'])

        # Separate cols for boolean options
        initial_cols = ['dem_education_level']
        final_cols = ['High_Ed', 'Low_Ed', 'Medium_Ed', 'No_Ed', 'Unknown_Ed']

        new_bool_df = m_ac.separate_df_to_bools(df_career_info, initial_cols, final_cols)
        df_career_info = df_career_info.join(other=new_bool_df, on=None, how='left', sort=False)

        # Dropping duplicate cols
        cols_to_del = ['dem_education_level']
        df_career_info.drop(columns=cols_to_del, inplace=True)

        # Save table into local folder
        m_ac.save_df_to_csv(df_career_info,
                       path='data/processed',    # Function adds hierarchy of files
                       name=f'career_info')      # Name of csv

        return df_career_info
    except:
        print('Something went wrong with [acquire_table_career_info]')

    finally:
        # Memory Usage and objects manually from Jupyter file
        print('''\n\t\t\t  >> Done cleaning df_career_info!. 
        \t\t\t | MEMORY USAGE \t|\t 301.7+ KB -->\t 207.4+ KB
        \t\t\t | DATA \t\t\t|\t objects(4) -->\t bool(6), object(2)
        \t\t\t\t  >> Chekout /data/processed/''')

def acquire_country_info(df_country_info):
    """Country info is list_of_dfs[1]"""
    try:
        print(f'\n\n· Cleaning df_country_info ....')
        # String Operations multiple inputs to binomial cols -> only 2 values from 2 options
        df_country_info['rural'] = m_ac.context_homogenization(df_country_info['rural'])

        # Separate cols for boolean options
        initial_cols = ['rural']
        final_cols = ['rural_context', 'urban_context']

        new_bool_df = m_ac.separate_df_to_bools(df_country_info, initial_cols, final_cols)
        df_country_info = df_country_info.join(other=new_bool_df,
                                               on=None,
                                               how='left',
                                               sort=False)

        df_country_info.drop(columns='rural', inplace=True)

        # Save table into local folder
        m_ac.save_df_to_csv(df_country_info,
                       path='data/processed',    # Function adds hierarchy of files
                       name=f'country_info')     # Name of csv

        return df_country_info

    except:
        print('Something went wrong with [acquire_career_info]')

    finally:
        print('''\n\t\t\t  >> Done cleaning df_country_info!.
        \t\t\t | MEMORY USAGE \t|\t FROM 337.0+ KB -->\t 226.3+ KB
        \t\t\t | DATA \t\t\t|\t FROM objects(5) -->\t object(3)
        \t\t\t\t  >> Chekout /data/processed/''')

def acquire_personal_info(df_personal_info):
    """Personal info is list_of-dfs[2]"""

    try:
        print(f'\n\n· Cleaning df_personal_info ....')
        # Number normalization
        df_personal_info['age'] = m_ac.ageStr_to_ageNum(serie= df_personal_info['age'])
        df_personal_info['age'] = m_ac.year_to_age(df_personal_info['age'])
        # df_personal_info['age'] = m_ac.year_update(df_personal_info['age']) NOT DONE

        # String Operations: multiple inputs in binomial cols -> only 2 values for 2 options
        df_personal_info['gender'] = m_ac.gender_homogenization(df_personal_info['gender'])
        df_personal_info['dem_has_children'] = m_ac.yes_no_to_bool(df_personal_info['dem_has_children'])

        # Separate cols for boolean options
        initial_cols = ['gender', 'age_group']
        final_cols = ['gender_Female', 'gender_Male', 'ageGroup_14_25', 'ageGroup_26_39', 'ageGroup_40_65',
                      'ageGroup_juvenile']

        new_bool_df = m_ac.separate_df_to_bools(df_personal_info, initial_cols, final_cols)
        df_personal_info = df_personal_info.join(other=new_bool_df, on=None, how='left', sort=False)

        # Save table into local folder
        m_ac.save_df_to_csv(df_personal_info,
                       path='data/processed',    # Function adds hierarchy of files
                       name='personal_info')    # Name of csv

        return df_personal_info

    except:
        print('Something went wrong with [acquire_table_personal_info]') # Make a log file

    finally:
        print('''\n\t\t\t  >> Done cleaning df_personal_info!. 
        \t\t\t | MEMORY USAGE \t|\t FROM 337.0+ KB -->\t 367.6+ KB
        \t\t\t | DATA \t\t\t|\t FROM objects(5) -->\t bool(7), object(4)
        \t\t\t\t  >> Chekout /data/processed/''')


def get_serie_at_split_str_at_char(ser, char):
    return [m_ac.split_str_at_char(response, char)
                                   if re.search(char, response)
                                   else response
                                   for response in ser]

def get_separate_df(serie_to_eval, separator_string, path_to_save_to, file_name):
    """
    INPUT   -> inputs to calls formentioned defs
    OUTPUT  -> saves them into a common zip file and return a list of alls dfs
    """
    print(f'\t ···· Iterating through poll lists')
    df_to_return = m_ac.multiple_choice_col_to_df( serie= serie_to_eval, separator= separator_string)
    m_ac.save_df_to_csv(df_to_return,
                        path=path_to_save_to,  # Function adds hierarchy of files
                        name=file_name)  # Name of csv

    return df_to_return

def acquire_poll_info(df):
    """Poll info is list_of-dfs[3]"""

    sep = ' | '  # this could change
    cols = [
        'question_bbi_2016wave4_basicincome_awareness',
        'question_bbi_2016wave4_basicincome_effect',
        'question_bbi_2016wave4_basicincome_vote',
        'question_bbi_2016wave4_basicincome_argumentsagainst',
        'question_bbi_2016wave4_basicincome_argumentsfor']

    files_names = ['poll_basicincome_awareness',
                   'poll_basicincome_effect',
                   'poll_basicincome_vote',
                   'poll_basicincome_argumentsagainst',
                   'poll_basicincome_argumentsfor']

    print(f'\n\n· Cleaning df_poll_info ....')

    # Deleting strange characters in column ------> this should be as a def in m_ac
    df['question_bbi_2016wave4_basicincome_effect'] = get_serie_at_split_str_at_char(ser= df['question_bbi_2016wave4_basicincome_effect'],
                                                                                     char= 'Û_ ')
    # Creating a list of series as an iterable, getting separate polls_info as iter and saving them into zip
    list_of_separated_polls = []
    for column, file_name in zip(cols, files_names):
        separated_polls = get_separate_df(serie_to_eval= df[column],
                                          separator_string= sep,
                                          path_to_save_to= 'data/processed/',
                                          file_name= file_name)
        list_of_separated_polls.append(separated_polls)

    return list_of_separated_polls


