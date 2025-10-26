"""
Data Analysis and Visualization Tool

This tool provides comprehensive data analysis capabilities including statistical analysis,
data manipulation, visualization creation, Excel file handling, CSV processing, and
advanced analytics. Supports pandas, numpy, matplotlib, seaborn, and plotly.
"""

import os
from typing import Dict, Any, Optional, List
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tools.base_tool import BaseTool


class DataAnalysisTool(BaseTool):
    """
    Advanced data analysis and visualization tool.
    
    Provides capabilities for loading data from various sources, performing statistical
    analysis, creating visualizations, manipulating datasets, and generating insights.
    Supports Excel, CSV, JSON, and SQL databases.
    """
    
    SUPPORTED_FORMATS = ['csv', 'excel', 'json', 'sql', 'parquet']
    CHART_TYPES = [
        'line', 'bar', 'scatter', 'histogram', 'box', 'violin',
        'heatmap', 'pie', 'area', '3d_scatter', 'correlation_matrix'
    ]
    
    def __init__(self, sandbox_path: str = "/tmp/graive_sandbox/data"):
        """
        Initialize the data analysis tool.
        
        Args:
            sandbox_path: Path to store data and visualizations
        """
        self.sandbox_path = sandbox_path
        os.makedirs(sandbox_path, exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "charts"), exist_ok=True)
        os.makedirs(os.path.join(sandbox_path, "reports"), exist_ok=True)
        
    @property
    def name(self) -> str:
        return "data_analysis"
    
    @property
    def description(self) -> str:
        return (
            "Analyze data, create visualizations, process Excel/CSV files, "
            "perform statistical analysis, generate insights, and create charts "
            "using pandas, matplotlib, seaborn, and plotly."
        )
    
    @property
    def schema(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "parameters": {
                "action": {
                    "type": "string",
                    "description": "Action to perform",
                    "enum": [
                        "load_data", "analyze", "visualize", "transform",
                        "statistics", "correlation", "export", "merge",
                        "filter", "group_by", "pivot"
                    ],
                    "required": True
                },
                "data_source": {
                    "type": "string",
                    "description": "Path to data file or SQL connection string",
                    "required": False
                },
                "format": {
                    "type": "string",
                    "description": "Data format",
                    "enum": ["csv", "excel", "json", "sql", "parquet"],
                    "required": False
                },
                "chart_type": {
                    "type": "string",
                    "description": "Type of visualization",
                    "enum": CHART_TYPES,
                    "required": False
                },
                "columns": {
                    "type": "array",
                    "description": "Columns to analyze or visualize",
                    "required": False
                },
                "parameters": {
                    "type": "object",
                    "description": "Additional parameters for the operation",
                    "required": False
                }
            }
        }
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """Validate parameters for data operations."""
        return "action" in parameters
    
    def execute(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute data analysis operation.
        
        Args:
            parameters: Operation parameters
            
        Returns:
            Operation result with analysis or visualization path
        """
        action = parameters["action"]
        
        action_map = {
            "load_data": self._load_data,
            "analyze": self._analyze_data,
            "visualize": self._create_visualization,
            "transform": self._transform_data,
            "statistics": self._calculate_statistics,
            "correlation": self._calculate_correlation,
            "export": self._export_data,
            "merge": self._merge_datasets,
            "filter": self._filter_data,
            "group_by": self._group_data,
            "pivot": self._pivot_data
        }
        
        handler = action_map.get(action)
        if handler:
            return handler(parameters)
        else:
            return {"error": f"Unknown action: {action}", "success": False}
    
    def _load_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Load data from file or database."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed. Install: pip install pandas",
                "success": False
            }
        
        try:
            data_source = params["data_source"]
            format_type = params.get("format", "csv")
            
            if format_type == "csv":
                df = pd.read_csv(data_source)
            elif format_type == "excel":
                df = pd.read_excel(data_source, engine='openpyxl')
            elif format_type == "json":
                df = pd.read_json(data_source)
            elif format_type == "parquet":
                df = pd.read_parquet(data_source)
            elif format_type == "sql":
                # SQL requires connection string
                import sqlalchemy
                engine = sqlalchemy.create_engine(params.get("connection_string"))
                df = pd.read_sql(params.get("query", "SELECT * FROM table"), engine)
            else:
                return {"error": f"Unsupported format: {format_type}", "success": False}
            
            # Store dataframe metadata
            info = {
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "sample": df.head(5).to_dict()
            }
            
            return {
                "success": True,
                "format": format_type,
                "info": info
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _analyze_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive data analysis."""
        load_result = self._load_data(params)
        
        if not load_result.get("success"):
            return load_result
        
        try:
            import pandas as pd
            import numpy as np
        except ImportError:
            return {
                "error": "Required packages not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            analysis = {
                "shape": {"rows": len(df), "columns": len(df.columns)},
                "columns": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "missing_values": df.isnull().sum().to_dict(),
                "numeric_summary": df.describe().to_dict() if len(df.select_dtypes(include=[np.number]).columns) > 0 else {},
                "categorical_summary": {},
                "duplicates": int(df.duplicated().sum())
            }
            
            # Analyze categorical columns
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                analysis["categorical_summary"][col] = {
                    "unique_values": int(df[col].nunique()),
                    "top_values": df[col].value_counts().head(5).to_dict()
                }
            
            return {
                "success": True,
                "analysis": analysis
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _create_visualization(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create data visualization."""
        try:
            import pandas as pd
            import matplotlib.pyplot as plt
            import seaborn as sns
        except ImportError:
            return {
                "error": "Required packages not installed. Install: pip install pandas matplotlib seaborn",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            chart_type = params.get("chart_type", "line")
            columns = params.get("columns", [])
            chart_params = params.get("parameters", {})
            
            plt.figure(figsize=(12, 6))
            
            if chart_type == "line":
                if len(columns) >= 1:
                    df[columns].plot(kind='line')
                else:
                    df.plot(kind='line')
                plt.title("Line Chart")
                
            elif chart_type == "bar":
                if len(columns) >= 1:
                    df[columns].plot(kind='bar')
                else:
                    df.plot(kind='bar')
                plt.title("Bar Chart")
                
            elif chart_type == "scatter":
                if len(columns) >= 2:
                    plt.scatter(df[columns[0]], df[columns[1]])
                    plt.xlabel(columns[0])
                    plt.ylabel(columns[1])
                plt.title("Scatter Plot")
                
            elif chart_type == "histogram":
                if len(columns) >= 1:
                    df[columns[0]].hist(bins=chart_params.get("bins", 30))
                else:
                    df.hist(bins=chart_params.get("bins", 30))
                plt.title("Histogram")
                
            elif chart_type == "box":
                if len(columns) >= 1:
                    df[columns].boxplot()
                else:
                    df.boxplot()
                plt.title("Box Plot")
                
            elif chart_type == "heatmap":
                correlation = df.select_dtypes(include=['number']).corr()
                sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0)
                plt.title("Correlation Heatmap")
                
            elif chart_type == "pie":
                if len(columns) >= 1:
                    df[columns[0]].value_counts().plot(kind='pie', autopct='%1.1f%%')
                plt.title("Pie Chart")
                
            elif chart_type == "correlation_matrix":
                correlation = df.select_dtypes(include=['number']).corr()
                sns.heatmap(correlation, annot=True, fmt='.2f', cmap='RdBu_r', center=0)
                plt.title("Correlation Matrix")
            
            # Save visualization
            filename = f"{chart_type}_{hash(str(columns)) % 10000}.png"
            filepath = os.path.join(self.sandbox_path, "charts", filename)
            plt.tight_layout()
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return {
                "success": True,
                "chart_type": chart_type,
                "chart_path": filepath,
                "columns_used": columns
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _calculate_statistics(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate detailed statistics."""
        try:
            import pandas as pd
            import numpy as np
            from scipy import stats
        except ImportError:
            return {
                "error": "Required packages not installed. Install: pip install pandas scipy",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            columns = params.get("columns", df.select_dtypes(include=[np.number]).columns.tolist())
            
            statistics = {}
            
            for col in columns:
                if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
                    col_data = df[col].dropna()
                    
                    statistics[col] = {
                        "count": int(len(col_data)),
                        "mean": float(col_data.mean()),
                        "median": float(col_data.median()),
                        "std": float(col_data.std()),
                        "var": float(col_data.var()),
                        "min": float(col_data.min()),
                        "max": float(col_data.max()),
                        "q25": float(col_data.quantile(0.25)),
                        "q75": float(col_data.quantile(0.75)),
                        "skewness": float(stats.skew(col_data)),
                        "kurtosis": float(stats.kurtosis(col_data))
                    }
            
            return {
                "success": True,
                "statistics": statistics
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _calculate_correlation(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate correlation matrix."""
        try:
            import pandas as pd
            import numpy as np
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            # Get numeric columns
            numeric_df = df.select_dtypes(include=[np.number])
            
            # Calculate correlation
            correlation = numeric_df.corr()
            
            return {
                "success": True,
                "correlation_matrix": correlation.to_dict(),
                "strong_correlations": self._find_strong_correlations(correlation)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _find_strong_correlations(self, corr_matrix, threshold=0.7):
        """Find strong correlations in correlation matrix."""
        strong_corr = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_value = corr_matrix.iloc[i, j]
                if abs(corr_value) >= threshold:
                    strong_corr.append({
                        "var1": corr_matrix.columns[i],
                        "var2": corr_matrix.columns[j],
                        "correlation": float(corr_value)
                    })
        
        return strong_corr
    
    def _transform_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Transform data (normalize, standardize, encode)."""
        try:
            import pandas as pd
            from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
        except ImportError:
            return {
                "error": "Required packages not installed. Install: pip install pandas scikit-learn",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            transformation = params.get("transformation", "normalize")
            columns = params.get("columns", df.select_dtypes(include=['number']).columns.tolist())
            
            if transformation == "normalize":
                scaler = MinMaxScaler()
                df[columns] = scaler.fit_transform(df[columns])
            
            elif transformation == "standardize":
                scaler = StandardScaler()
                df[columns] = scaler.fit_transform(df[columns])
            
            elif transformation == "encode":
                for col in columns:
                    if df[col].dtype == 'object':
                        le = LabelEncoder()
                        df[col] = le.fit_transform(df[col])
            
            # Save transformed data
            filename = f"transformed_{hash(params['data_source']) % 10000}.csv"
            filepath = os.path.join(self.sandbox_path, filename)
            df.to_csv(filepath, index=False)
            
            return {
                "success": True,
                "transformation": transformation,
                "output_file": filepath,
                "columns_transformed": columns
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _export_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Export data to various formats."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            export_format = params.get("export_format", "csv")
            filename = params.get("filename", f"export_{hash(params['data_source']) % 10000}")
            
            if export_format == "csv":
                filepath = os.path.join(self.sandbox_path, f"{filename}.csv")
                df.to_csv(filepath, index=False)
            
            elif export_format == "excel":
                filepath = os.path.join(self.sandbox_path, f"{filename}.xlsx")
                df.to_excel(filepath, index=False, engine='openpyxl')
            
            elif export_format == "json":
                filepath = os.path.join(self.sandbox_path, f"{filename}.json")
                df.to_json(filepath, orient='records', indent=2)
            
            elif export_format == "html":
                filepath = os.path.join(self.sandbox_path, f"{filename}.html")
                df.to_html(filepath, index=False)
            
            else:
                return {"error": f"Unsupported export format: {export_format}", "success": False}
            
            return {
                "success": True,
                "export_format": export_format,
                "output_file": filepath
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _filter_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Filter data based on conditions."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            conditions = params.get("conditions", {})
            
            for column, condition in conditions.items():
                if column in df.columns:
                    operator = condition.get("operator", "==")
                    value = condition.get("value")
                    
                    if operator == "==":
                        df = df[df[column] == value]
                    elif operator == ">":
                        df = df[df[column] > value]
                    elif operator == "<":
                        df = df[df[column] < value]
                    elif operator == ">=":
                        df = df[df[column] >= value]
                    elif operator == "<=":
                        df = df[df[column] <= value]
                    elif operator == "!=":
                        df = df[df[column] != value]
                    elif operator == "contains":
                        df = df[df[column].str.contains(str(value), na=False)]
            
            # Save filtered data
            filename = f"filtered_{hash(str(conditions)) % 10000}.csv"
            filepath = os.path.join(self.sandbox_path, filename)
            df.to_csv(filepath, index=False)
            
            return {
                "success": True,
                "rows_before": len(pd.read_csv(params["data_source"])),
                "rows_after": len(df),
                "output_file": filepath
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _group_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Group data and calculate aggregations."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            group_by = params.get("group_by", [])
            aggregations = params.get("aggregations", {"count": "size"})
            
            grouped = df.groupby(group_by).agg(aggregations)
            
            # Save grouped data
            filename = f"grouped_{hash(str(group_by)) % 10000}.csv"
            filepath = os.path.join(self.sandbox_path, filename)
            grouped.to_csv(filepath)
            
            return {
                "success": True,
                "groups": len(grouped),
                "output_file": filepath,
                "sample": grouped.head(10).to_dict()
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _pivot_data(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Create pivot table from data."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            df = pd.read_csv(params["data_source"]) if params.get("format", "csv") == "csv" else pd.read_excel(params["data_source"])
            
            index = params.get("index")
            columns = params.get("pivot_columns")
            values = params.get("values")
            aggfunc = params.get("aggfunc", "mean")
            
            pivot = pd.pivot_table(df, values=values, index=index, columns=columns, aggfunc=aggfunc)
            
            # Save pivot table
            filename = f"pivot_{hash(str(index)) % 10000}.csv"
            filepath = os.path.join(self.sandbox_path, filename)
            pivot.to_csv(filepath)
            
            return {
                "success": True,
                "output_file": filepath,
                "shape": pivot.shape,
                "sample": pivot.head(10).to_dict()
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
    
    def _merge_datasets(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Merge multiple datasets."""
        try:
            import pandas as pd
        except ImportError:
            return {
                "error": "Pandas not installed",
                "success": False
            }
        
        try:
            sources = params.get("sources", [])
            merge_on = params.get("merge_on")
            how = params.get("how", "inner")
            
            dfs = []
            for source in sources:
                if source.endswith('.csv'):
                    dfs.append(pd.read_csv(source))
                elif source.endswith(('.xlsx', '.xls')):
                    dfs.append(pd.read_excel(source))
            
            if len(dfs) < 2:
                return {"error": "Need at least 2 datasets to merge", "success": False}
            
            # Merge datasets
            merged = dfs[0]
            for df in dfs[1:]:
                merged = pd.merge(merged, df, on=merge_on, how=how)
            
            # Save merged data
            filename = f"merged_{hash(str(sources)) % 10000}.csv"
            filepath = os.path.join(self.sandbox_path, filename)
            merged.to_csv(filepath, index=False)
            
            return {
                "success": True,
                "output_file": filepath,
                "rows": len(merged),
                "columns": len(merged.columns)
            }
            
        except Exception as e:
            return {"error": str(e), "success": False}
