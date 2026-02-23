"""
数据处理服务
包含各种数据处理和分析的业务逻辑
"""
import asyncio
import random
from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from beartype import beartype
from models.base_model import TaskStatus


class DataService:
    """
    数据处理服务类
    提供各种数据处理、分析和模拟操作
    """
    
    @beartype
    def __init__(self, progress_callback: Optional[Callable[[float, str], None]] = None):
        """
        初始化数据服务
        
        Args:
            progress_callback: 进度回调函数
        """
        self.progress_callback = progress_callback
    
    @beartype
    def _update_progress(self, progress: float, message: str) -> None:
        """
        更新进度
        
        Args:
            progress: 进度百分比
            message: 进度消息
        """
        if self.progress_callback:
            self.progress_callback(progress, message)
    
    @beartype
    async def process_large_dataset(
        self, 
        data_size: int = 1000,
        processing_delay: float = 0.01
    ) -> Dict[str, Any]:
        """
        处理大型数据集
        模拟耗时的数据处理操作
        
        Args:
            data_size: 数据集大小
            processing_delay: 每项处理延迟（秒）
            
        Returns:
            Dict[str, Any]: 处理结果
        """
        self._update_progress(0, "初始化数据处理...")
        
        # 生成模拟数据
        dataset = [
            {
                "id": i,
                "value": random.randint(1, 1000),
                "category": random.choice(["A", "B", "C", "D"]),
                "timestamp": datetime.now() - timedelta(days=random.randint(0, 365))
            }
            for i in range(data_size)
        ]
        
        self._update_progress(10, f"生成了 {data_size} 条数据，开始处理...")
        
        # 处理数据
        processed_data = []
        category_stats = {}
        value_sum = 0
        
        for i, item in enumerate(dataset):
            # 模拟处理时间
            if processing_delay > 0:
                await asyncio.sleep(processing_delay)
            
            # 数据处理逻辑
            processed_item = {
                "id": item["id"],
                "processed_value": item["value"] * 1.1,  # 增加10%
                "category": item["category"],
                "is_high_value": item["value"] > 500,
                "age_days": (datetime.now() - item["timestamp"]).days
            }
            
            processed_data.append(processed_item)
            
            # 统计信息
            category = item["category"]
            if category not in category_stats:
                category_stats[category] = {"count": 0, "total_value": 0}
            
            category_stats[category]["count"] += 1
            category_stats[category]["total_value"] += item["value"]
            value_sum += item["value"]
            
            # 更新进度
            progress = 10 + (i + 1) / data_size * 80
            if i % 50 == 0 or i == data_size - 1:  # 每50项或最后一项更新进度
                self._update_progress(progress, f"已处理 {i + 1}/{data_size} 项数据")
        
        self._update_progress(95, "生成处理报告...")
        
        # 生成统计报告
        report = {
            "processing_completed_at": datetime.now().isoformat(),
            "total_items": data_size,
            "processing_time_estimate": data_size * processing_delay,
            "statistics": {
                "total_value": value_sum,
                "average_value": value_sum / data_size,
                "high_value_items": len([item for item in processed_data if item["is_high_value"]]),
                "category_breakdown": {
                    cat: {
                        "count": stats["count"],
                        "percentage": (stats["count"] / data_size) * 100,
                        "average_value": stats["total_value"] / stats["count"]
                    }
                    for cat, stats in category_stats.items()
                }
            },
            "sample_data": processed_data[:10]  # 前10项作为样本
        }
        
        self._update_progress(100, "数据处理完成")
        
        return report
    
    @beartype
    async def analyze_trends(self, time_series_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        分析趋势数据
        对时间序列数据进行趋势分析
        
        Args:
            time_series_data: 时间序列数据
            
        Returns:
            Dict[str, Any]: 趋势分析结果
        """
        self._update_progress(0, "开始趋势分析...")
        
        if not time_series_data:
            # 生成模拟时间序列数据
            self._update_progress(20, "生成模拟数据...")
            time_series_data = self._generate_time_series_data()
        
        self._update_progress(40, "计算趋势指标...")
        
        # 模拟复杂计算
        await asyncio.sleep(1)
        
        # 提取数值
        values = [item.get("value", 0) for item in time_series_data]
        
        # 计算趋势指标
        if len(values) < 2:
            trend = "insufficient_data"
            trend_strength = 0
        else:
            # 简单线性趋势计算
            n = len(values)
            x_mean = (n - 1) / 2
            y_mean = sum(values) / n
            
            numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((i - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                slope = 0
            else:
                slope = numerator / denominator
            
            if slope > 0.1:
                trend = "increasing"
            elif slope < -0.1:
                trend = "decreasing"
            else:
                trend = "stable"
            
            trend_strength = abs(slope)
        
        self._update_progress(70, "计算统计指标...")
        
        # 统计指标
        stats = {
            "count": len(values),
            "min": min(values) if values else 0,
            "max": max(values) if values else 0,
            "mean": sum(values) / len(values) if values else 0,
            "median": sorted(values)[len(values) // 2] if values else 0
        }
        
        # 计算标准差
        if len(values) > 1:
            variance = sum((x - stats["mean"]) ** 2 for x in values) / (len(values) - 1)
            stats["std_dev"] = variance ** 0.5
        else:
            stats["std_dev"] = 0
        
        self._update_progress(90, "生成分析报告...")
        
        # 模拟报告生成时间
        await asyncio.sleep(0.5)
        
        analysis_result = {
            "analysis_completed_at": datetime.now().isoformat(),
            "data_points": len(time_series_data),
            "trend_analysis": {
                "trend_direction": trend,
                "trend_strength": trend_strength,
                "confidence": min(0.95, trend_strength * 10)  # 模拟置信度
            },
            "statistical_summary": stats,
            "anomalies": self._detect_anomalies(values, stats["mean"], stats["std_dev"]),
            "recommendations": self._generate_recommendations(trend, trend_strength)
        }
        
        self._update_progress(100, "趋势分析完成")
        
        return analysis_result
    
    @beartype
    def _generate_time_series_data(self, points: int = 100) -> List[Dict[str, Any]]:
        """
        生成模拟时间序列数据
        
        Args:
            points: 数据点数量
            
        Returns:
            List[Dict[str, Any]]: 时间序列数据
        """
        base_value = 100
        trend = random.uniform(-0.5, 0.5)
        noise_level = 10
        
        data = []
        for i in range(points):
            # 基础趋势 + 随机噪声 + 季节性变化
            value = (
                base_value + 
                trend * i + 
                random.gauss(0, noise_level) +
                10 * random.sin(i * 0.1)  # 季节性变化
            )
            
            data.append({
                "timestamp": (datetime.now() - timedelta(days=points-i)).isoformat(),
                "value": max(0, value),  # 确保非负值
                "index": i
            })
        
        return data
    
    @beartype
    def _detect_anomalies(
        self, 
        values: List[float], 
        mean: float, 
        std_dev: float
    ) -> List[Dict[str, Any]]:
        """
        检测异常值
        
        Args:
            values: 数值列表
            mean: 平均值
            std_dev: 标准差
            
        Returns:
            List[Dict[str, Any]]: 异常值列表
        """
        if std_dev == 0:
            return []
        
        threshold = 2.0  # 2个标准差
        anomalies = []
        
        for i, value in enumerate(values):
            z_score = abs(value - mean) / std_dev
            if z_score > threshold:
                anomalies.append({
                    "index": i,
                    "value": value,
                    "z_score": z_score,
                    "type": "high" if value > mean else "low"
                })
        
        return anomalies
    
    @beartype
    def _generate_recommendations(self, trend: str, strength: float) -> List[str]:
        """
        生成建议
        
        Args:
            trend: 趋势方向
            strength: 趋势强度
            
        Returns:
            List[str]: 建议列表
        """
        recommendations = []
        
        if trend == "increasing":
            if strength > 0.5:
                recommendations.append("数据呈现强烈上升趋势，建议继续当前策略")
                recommendations.append("考虑扩大投入以维持增长势头")
            else:
                recommendations.append("数据呈现温和上升趋势，保持观察")
        elif trend == "decreasing":
            if strength > 0.5:
                recommendations.append("数据呈现明显下降趋势，需要立即采取行动")
                recommendations.append("建议分析下降原因并制定改进措施")
            else:
                recommendations.append("数据略有下降，建议密切监控")
        else:
            recommendations.append("数据相对稳定，可以考虑优化现有流程")
            recommendations.append("稳定期是进行创新和改进的好时机")
        
        recommendations.append("建议定期更新数据以保持分析的准确性")
        
        return recommendations
    
    @beartype
    async def export_data(
        self, 
        data: List[Dict[str, Any]], 
        format_type: str = "json"
    ) -> Dict[str, Any]:
        """
        导出数据
        模拟数据导出操作
        
        Args:
            data: 要导出的数据
            format_type: 导出格式 ("json", "csv", "excel")
            
        Returns:
            Dict[str, Any]: 导出结果
        """
        self._update_progress(0, f"开始导出数据为 {format_type} 格式...")
        
        # 模拟导出处理时间
        total_items = len(data)
        
        for i in range(0, total_items, 100):  # 每100项更新一次进度
            progress = (i / total_items) * 90
            self._update_progress(progress, f"已处理 {min(i + 100, total_items)}/{total_items} 项")
            await asyncio.sleep(0.1)  # 模拟处理时间
        
        self._update_progress(95, "生成导出文件...")
        
        # 模拟文件生成
        await asyncio.sleep(0.5)
        
        # 生成导出结果
        export_result = {
            "export_completed_at": datetime.now().isoformat(),
            "format": format_type,
            "total_records": total_items,
            "file_size_estimate": f"{total_items * 0.1:.1f} KB",
            "export_path": f"exports/data_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_type}",
            "checksum": f"md5:{hash(str(data)) % 1000000:06d}",  # 模拟校验和
            "metadata": {
                "exported_by": "DataService",
                "version": "1.0",
                "encoding": "utf-8"
            }
        }
        
        self._update_progress(100, "数据导出完成")
        
        return export_result
