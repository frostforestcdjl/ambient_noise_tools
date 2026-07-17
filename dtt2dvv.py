import os
import pandas as pd

path = '../DTT'

filters = os.listdir(path)

for filterid in filters:
    stack_days = os.listdir(os.path.join(path, filterid))
    for mov_stack in stack_days:
        Dates = []
        dvv_M_lst = []
        dvv_M0_lst = []
        pair_lst = []
        components = os.listdir(os.path.join(path, filterid, mov_stack))
        for component in components:
            files = os.listdir(os.path.join(path, filterid, mov_stack, component))
            files = [file for file in files if file.endswith('.txt')]
            files.sort()
            for file in files:
                df = pd.read_csv(os.path.join(path, filterid, mov_stack, component, file))
                Date = df['Date'].values
                pair = df['Pairs'].values
                M = df['M'].values
                M0 = df['M0'].values
                if len(M) > 0 and len(M0) > 0:
                    Dates.append(Date[0])
                    dvv_M_lst.append(-1*M[0])
                    dvv_M0_lst.append(-1*M0[0])
                    pair_lst.append(pair[0])

            pair_lst = list(set(pair_lst))
            if len(pair_lst) > 1:
                print(f"Warning: Multiple pairs found in {filterid}/{mov_stack}/{component}: {pair_lst}")

            output = os.path.join(
            '..',
            'DVV', 
            "%02i" % filterid, 
            f"%03i_DAYS" % mov_stack,
            components)

            df_out = pd.DataFrame(
                            {'dvv_M': dvv_M_lst, 'dvv_M0': dvv_M0_lst},
                            index=Dates)
            
            os.makedirs(output, exist_ok=True)
            df_out.to_csv(os.path.join(output, f'{pair_lst[0]}.txt'))