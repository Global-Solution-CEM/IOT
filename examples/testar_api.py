"""
Exemplos de uso da API de recomendações de cursos com IA
Execute este script para testar a API localmente
"""

import requests
import json
from typing import Dict, Any

# URL base da API
BASE_URL = "http://localhost:8000"


def print_response(response: requests.Response, title: str = "Response"):
    """Imprime resposta formatada"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)


def test_health_check():
    """Testa o health check da API"""
    print("\nTestando Health Check...")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")
    return response.status_code == 200


def test_root():
    """Testa o endpoint raiz"""
    print("\nTestando Endpoint Raiz...")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Root Endpoint")
    return response.status_code == 200


def test_analyze_profile():
    """Testa análise de perfil com IA"""
    print("\nTestando Análise de Perfil com IA...")
    
    profile_data = {
        "user_id": "test_user_123",
        "name": "João Silva",
        "email": "joao@example.com",
        "areas_interesse": [
            {
                "area": "programacao",
                "nivel": "intermediario"
            },
            {
                "area": "ia",
                "nivel": "iniciante"
            }
        ],
        "cursos_completos": ["1", "5"],
        "cursos_em_andamento": ["2"],
        "progresso_cursos": {
            "2": 45
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/ai/analyze-profile",
        json=profile_data,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "Análise de Perfil")
    return response.status_code == 200


def test_get_recommendations():
    """Testa geração de recomendações de cursos com IA"""
    print("\nTestando Geração de Recomendações com IA...")
    
    request_data = {
        "user_profile": {
            "user_id": "test_user_123",
            "name": "João Silva",
            "email": "joao@example.com",
            "areas_interesse": [
                {
                    "area": "programacao",
                    "nivel": "intermediario"
                },
                {
                    "area": "ia",
                    "nivel": "iniciante"
                }
            ],
            "cursos_completos": ["1", "5"],
            "cursos_em_andamento": ["2"],
            "progresso_cursos": {
                "2": 45
            }
        },
        "limit": 5
    }
    
    response = requests.post(
        f"{BASE_URL}/api/courses/suggested/test_user_123",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "Recomendações de Cursos")
    return response.status_code == 200


def test_generate_explanation():
    """Testa geração de explicação personalizada"""
    print("\nTestando Geração de Explicação...")
    
    data = {
        "course": {
            "id": "3",
            "titulo": "Desenvolvimento Web Full Stack",
            "descricao": "Aprenda a criar aplicações web completas com React, Node.js e bancos de dados.",
            "area": "programacao",
            "nivel": "intermediario",
            "duracao": "80 horas",
            "icone": "💻"
        },
        "user_profile": {
            "user_id": "test_user_123",
            "areas_interesse": [
                {"area": "programacao", "nivel": "intermediario"}
            ]
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/api/ai/generate-explaination",
        json=data,
        headers={"Content-Type": "application/json"}
    )
    
    print_response(response, "Explicação Gerada")
    return response.status_code == 200


def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("TESTES DA API DE RECOMENDAÇÕES COM IA")
    print("="*60)
    print("\nCertifique-se de que o servidor está rodando em http://localhost:8000")
    print("\nPressione Enter para continuar...")
    input()
    
    # Lista de testes
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root),
        ("Análise de Perfil", test_analyze_profile),
        ("Recomendações", test_get_recommendations),
        ("Explicação", test_generate_explanation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except requests.exceptions.ConnectionError:
            print(f"\nErro: Não foi possível conectar ao servidor em {BASE_URL}")
            print("   Certifique-se de que o servidor está rodando.")
            results.append((test_name, False))
        except Exception as e:
            print(f"\nErro ao executar {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    for test_name, success in results:
        status = "PASSOU" if success else "FALHOU"
        print(f"{test_name}: {status}")
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    print(f"\nTotal: {passed}/{total} testes passaram")


if __name__ == "__main__":
    main()


