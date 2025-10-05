"""
Dashboard de Monitoramento em Tempo Real
=========================================
Exibe métricas da API no terminal

Uso:
    python dashboard.py
"""

import requests
import time
from datetime import datetime
import sys


BASE_URL = "http://localhost:8000/api/v1"


def clear_screen():
    """Limpa a tela do terminal"""
    print("\033[2J\033[H", end="")


def get_color(value, threshold_good, threshold_bad):
    """Retorna cor baseada em thresholds"""
    if value <= threshold_good:
        return "\033[32m"  # Verde
    elif value <= threshold_bad:
        return "\033[33m"  # Amarelo
    else:
        return "\033[31m"  # Vermelho


def display_dashboard():
    """Exibe dashboard de métricas no terminal"""
    
    while True:
        try:
            # Limpar tela
            clear_screen()
            
            # Header
            print("=" * 100)
            print(f"📊 BOOKS SCRAPER API - MONITORING DASHBOARD".center(100))
            print(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}".center(100))
            print("=" * 100)
            
            # Obter métricas
            metrics_response = requests.get(f"{BASE_URL}/metrics", timeout=5)
            health_response = requests.get(f"{BASE_URL}/health", timeout=5)
            
            if metrics_response.status_code != 200:
                print("\n❌ Erro ao obter métricas da API")
                print(f"Status Code: {metrics_response.status_code}")
                time.sleep(5)
                continue
            
            metrics = metrics_response.json()
            health = health_response.json()
            
            # Seção 1: Overview
            print(f"\n{'📈 OVERVIEW':<50}")
            print("-" * 100)
            
            error_rate = metrics['error_rate']
            error_color = get_color(error_rate, 1.0, 5.0)
            
            print(f"  Total Requests:  {metrics['total_requests']:>10,}")
            print(f"  Total Errors:    {metrics['total_errors']:>10,}")
            print(f"  Error Rate:      {error_color}{error_rate:>9.2f}%\033[0m")
            
            # Seção 2: Requests por Método
            print(f"\n{'🔀 REQUESTS POR MÉTODO':<50}")
            print("-" * 100)
            
            max_count = max(metrics['requests_by_method'].values()) if metrics['requests_by_method'] else 1
            
            for method, count in sorted(metrics['requests_by_method'].items()):
                bar_length = int((count / max_count) * 40)
                bar = "█" * bar_length
                percentage = (count / metrics['total_requests']) * 100
                print(f"  {method:8s}: {bar:<40} {count:>6} ({percentage:5.1f}%)")
            
            # Seção 3: Top Endpoints
            print(f"\n{'🔥 TOP 10 ENDPOINTS':<50}")
            print("-" * 100)
            
            for i, (endpoint, count) in enumerate(
                list(metrics['requests_by_endpoint'].items())[:10], 1
            ):
                percentage = (count / metrics['total_requests']) * 100
                print(f"  {i:2d}. {endpoint[:70]:<70} {count:>6} ({percentage:5.1f}%)")
            
            # Seção 4: Status Codes
            print(f"\n{'📊 HTTP STATUS CODES':<50}")
            print("-" * 100)
            
            status_groups = {
                '2xx ✅': sum(v for k, v in metrics['status_codes'].items() if 200 <= int(k) < 300),
                '3xx ↪️ ': sum(v for k, v in metrics['status_codes'].items() if 300 <= int(k) < 400),
                '4xx ⚠️ ': sum(v for k, v in metrics['status_codes'].items() if 400 <= int(k) < 500),
                '5xx ❌': sum(v for k, v in metrics['status_codes'].items() if 500 <= int(k) < 600),
            }
            
            for group, count in status_groups.items():
                if count > 0:
                    percentage = (count / metrics['total_requests']) * 100
                    print(f"  {group}: {count:>6} ({percentage:5.1f}%)")
            
            # Seção 5: Performance
            print(f"\n{'⚡ PERFORMANCE METRICS':<50}")
            print("-" * 100)
            
            rt = metrics['response_times']
            
            # Colorir baseado em thresholds
            mean_color = get_color(rt['mean'], 0.1, 0.5)
            p95_color = get_color(rt['p95'], 0.5, 1.0)
            p99_color = get_color(rt['p99'], 1.0, 2.0)
            
            print(f"  Requests Sampled: {rt['count']:>10,}")
            print(f"  Mean Response:    {mean_color}{rt['mean']:>9.4f}s\033[0m")
            print(f"  Median Response:  {rt['median']:>9.4f}s")
            print(f"  P95 Response:     {p95_color}{rt['p95']:>9.4f}s\033[0m")
            print(f"  P99 Response:     {p99_color}{rt['p99']:>9.4f}s\033[0m")
            print(f"  Min Response:     {rt['min']:>9.4f}s")
            print(f"  Max Response:     {rt['max']:>9.4f}s")
            
            # Seção 6: Health
            print(f"\n{'❤️  HEALTH STATUS':<50}")
            print("-" * 100)
            
            if health['status'] == 'healthy':
                status_display = "\033[32m🟢 HEALTHY\033[0m"
            else:
                status_display = "\033[31m🔴 UNHEALTHY\033[0m"
            
            print(f"  Status:           {status_display}")
            print(f"  Total Books:      {health['database']['total_books']:>10,}")
            print(f"  Database File:    {health['database']['file_exists']}")
            print(f"  Cache Valid:      {health['database'].get('cache_valid', 'N/A')}")
            
            # Seção 7: Alertas
            print(f"\n{'🚨 ALERTS':<50}")
            print("-" * 100)
            
            alerts = []
            
            if error_rate > 5.0:
                alerts.append(f"  ⚠️  High error rate: {error_rate:.2f}%")
            
            if rt['p95'] > 1.0:
                alerts.append(f"  ⚠️  Slow P95 response time: {rt['p95']:.4f}s")
            
            if rt['mean'] > 0.5:
                alerts.append(f"  ⚠️  High mean response time: {rt['mean']:.4f}s")
            
            if metrics['total_errors'] > 100:
                alerts.append(f"  ⚠️  Too many errors: {metrics['total_errors']}")
            
            if health['status'] != 'healthy':
                alerts.append(f"  ❌ API is unhealthy!")
            
            if alerts:
                for alert in alerts:
                    print(alert)
            else:
                print("  ✅ No alerts - All systems operational")
            
            # Footer
            print("\n" + "=" * 100)
            print("Press Ctrl+C to exit | Refreshing every 5 seconds...".center(100))
            print("=" * 100)
            
            time.sleep(5)
            
        except requests.exceptions.ConnectionError:
            clear_screen()
            print("\n" + "=" * 100)
            print("❌ ERRO: Não foi possível conectar à API".center(100))
            print("=" * 100)
            print("\nVerifique se a API está rodando:")
            print("  python run.py")
            print("\nTentando reconectar em 5 segundos...")
            time.sleep(5)
            
        except KeyboardInterrupt:
            print("\n\n" + "=" * 100)
            print("👋 Dashboard encerrado".center(100))
            print("=" * 100 + "\n")
            sys.exit(0)
            
        except Exception as e:
            print(f"\n\n❌ Erro inesperado: {e}")
            print("Tentando novamente em 5 segundos...")
            time.sleep(5)


if __name__ == "__main__":
    print("\n🚀 Iniciando Dashboard de Monitoramento...")
    print("Conectando à API em " + BASE_URL)
    time.sleep(1)
    
    try:
        # Teste inicial de conexão
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Conexão estabelecida!\n")
            time.sleep(1)
            display_dashboard()
        else:
            print(f"❌ API retornou status {response.status_code}")
            print("Verifique se a API está funcionando corretamente.")
            sys.exit(1)
            
    except requests.exceptions.ConnectionError:
        print("❌ Não foi possível conectar à API")
        print("\nVerifique se a API está rodando:")
        print("  python run.py")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Cancelado pelo usuário")
        sys.exit(0)