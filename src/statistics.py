import pandas as pd
import numpy as np
from scipy import stats


def calculate_pearson_correlation(series_x: pd.Series, series_y: pd.Series) -> dict:
    """
    Calculates Pearson Correlation coefficient and p-value.
    Returns structured results dictionary.
    """
    clean_df = pd.concat([series_x, series_y], axis=1).dropna()
    if len(clean_df) < 3:
        return {
            "r": 0.0,
            "p_value": 1.0,
            "sample_size": len(clean_df),
            "strength": "Insufficient data",
            "direction": "N/A",
            "statistically_significant": False,
            "interpretation": "Insufficient sample size (minimum 3 records required)."
        }

    x = clean_df.iloc[:, 0].values
    y = clean_df.iloc[:, 1].values

    r, p_val = stats.pearsonr(x, y)

    # Determine direction
    if abs(r) < 0.05:
        direction = "Neutral"
    elif r > 0:
        direction = "Positive"
    else:
        direction = "Negative"

    # Determine strength
    abs_r = abs(r)
    if abs_r < 0.1:
        strength = "Negligible"
    elif abs_r < 0.3:
        strength = "Weak"
    elif abs_r < 0.5:
        strength = "Moderate"
    elif abs_r < 0.7:
        strength = "Strong"
    else:
        strength = "Very Strong"

    sig = bool(p_val < 0.05)

    interpretation = (
        f"A {strength.lower()} {direction.lower()} Pearson correlation (r = {r:.3f}, p = {p_val:.4f}) "
        f"was observed across n = {len(clean_df)} students. "
        f"The relationship is {'statistically significant (p < 0.05)' if sig else 'not statistically significant (p ≥ 0.05)'}."
    )

    return {
        "r": round(float(r), 4),
        "p_value": round(float(p_val), 5),
        "sample_size": len(clean_df),
        "strength": strength,
        "direction": direction,
        "statistically_significant": sig,
        "interpretation": interpretation
    }


def calculate_spearman_correlation(series_x: pd.Series, series_y: pd.Series) -> dict:
    """
    Calculates Spearman Rank Correlation coefficient and p-value.
    """
    clean_df = pd.concat([series_x, series_y], axis=1).dropna()
    if len(clean_df) < 3:
        return {
            "rho": 0.0,
            "p_value": 1.0,
            "sample_size": len(clean_df),
            "strength": "Insufficient data",
            "direction": "N/A",
            "statistically_significant": False,
            "interpretation": "Insufficient sample size (minimum 3 records required)."
        }

    x = clean_df.iloc[:, 0].values
    y = clean_df.iloc[:, 1].values

    rho, p_val = stats.spearmanr(x, y)

    abs_rho = abs(rho)
    if abs_rho < 0.1:
        strength = "Negligible"
    elif abs_rho < 0.3:
        strength = "Weak"
    elif abs_rho < 0.5:
        strength = "Moderate"
    elif abs_rho < 0.7:
        strength = "Strong"
    else:
        strength = "Very Strong"

    direction = "Positive" if rho > 0 else ("Negative" if rho < 0 else "Neutral")
    sig = bool(p_val < 0.05)

    interpretation = (
        f"A {strength.lower()} {direction.lower()} monotonic relationship (Spearman ρ = {rho:.3f}, p = {p_val:.4f}) "
        f"was identified. Result is {'statistically significant' if sig else 'not statistically significant'}."
    )

    return {
        "rho": round(float(rho), 4),
        "p_value": round(float(p_val), 5),
        "sample_size": len(clean_df),
        "strength": strength,
        "direction": direction,
        "statistically_significant": sig,
        "interpretation": interpretation
    }


def calculate_descriptive_stats(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Computes mean, median, mode, standard deviation, min, max, quartiles (Q1, Q2, Q3), IQR.
    """
    if df.empty:
        return pd.DataFrame()

    if columns is None:
        columns = ["social_media_hours", "study_hours", "academic_marks", "sleep_hours", "attendance"]

    valid_cols = [c for c in columns if c in df.columns]
    if not valid_cols:
        return pd.DataFrame()

    stats_list = []
    for col in valid_cols:
        series = df[col].dropna()
        if series.empty:
            continue

        mean_val = series.mean()
        median_val = series.median()
        mode_res = series.mode()
        mode_val = mode_res.iloc[0] if not mode_res.empty else np.nan
        std_val = series.std()
        min_val = series.min()
        max_val = series.max()
        q1 = series.quantile(0.25)
        q2 = series.quantile(0.50)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        stats_list.append({
            "Variable": col.replace("_", " ").title(),
            "Count": len(series),
            "Mean": round(mean_val, 2),
            "Median": round(median_val, 2),
            "Mode": round(mode_val, 2),
            "Std Dev": round(std_val, 2),
            "Min": round(min_val, 2),
            "Q1 (25%)": round(q1, 2),
            "Q2 (50%)": round(q2, 2),
            "Q3 (75%)": round(q3, 2),
            "Max": round(max_val, 2),
            "IQR": round(iqr, 2)
        })

    return pd.DataFrame(stats_list)


def calculate_correlation_matrix(df: pd.DataFrame, columns: list = None) -> pd.DataFrame:
    """
    Computes standard Pearson correlation matrix for numerical metrics.
    """
    if df.empty:
        return pd.DataFrame()

    if columns is None:
        columns = ["social_media_hours", "study_hours", "academic_marks", "sleep_hours", "attendance"]

    valid_cols = [c for c in columns if c in df.columns]
    if len(valid_cols) < 2:
        return pd.DataFrame()

    corr_matrix = df[valid_cols].corr(method='pearson')
    # Clean variable labels
    display_names = {col: col.replace("_", " ").title() for col in valid_cols}
    corr_matrix = corr_matrix.rename(index=display_names, columns=display_names)
    return corr_matrix.round(3)
