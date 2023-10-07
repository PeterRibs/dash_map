def categorizing(df, coluna):
    diff = df[f'{coluna}'].max() - df[f'{coluna}'].min()

    category_ranges = [(df[f'{coluna}'].min() + i * diff / 5, df[f'{coluna}'].min() + (i+1) * diff / 5) for i in range(5)]
    categories = [f"({r[0]} - {r[1]})" for i, r in enumerate(category_ranges)]

    def get_category(row):
        for r, label in zip(category_ranges, categories):
            if r[0] <= row <= r[1]:
                return label
        return None

    df[f'{coluna}_cat'] = df[f'{coluna}'].apply(get_category)

    return df