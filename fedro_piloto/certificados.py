"""Certificados de proveniência "descoberta" (barreira por construção contra soluções manuais).

Uma Solucao, um Fragmento ou uma entrada de biblioteca só pode ser "descoberta" se vier com um
certificado emitido pelo laço do aprendiz:
  1. CertificadoBusca: emitido SÓ por enumerador.EstadoBusca.buscar quando devolve um termo (o termo
     saiu da enumeração, não de um parse ou de programas_referencia);
  2. CertificadoDescoberta: emitido SÓ por aprendizes.AprendizBase.resolver quando o oráculo aceita
     esse termo; liga o termo ao certificado de busca, à tarefa, ao aprendiz e ao índice do
     ResultadoTarefa aceito;
  3. CertificadoEntrada: emitido SÓ por biblioteca.Biblioteca (modo "autonomo") ao criar uma
     entrada a partir de um corpus em que toda solução tem CertificadoDescoberta válido; exigido por
     dsl.Tabela.adicionar para entradas "descoberta" numa tabela de uso "descoberta".
Cada certificado leva um selo HMAC-SHA256 com uma chave aleatória do processo (não persistida) sobre
o seu conteúdo; um certificado construído à mão, ou copiado de outro termo, não verifica. As funções
emitir_* conferem o chamador (módulo e função); é a garantia possível em Python: contorná-la exige
importar a chave privada do módulo deliberadamente.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import sys
from dataclasses import dataclass
from typing import Optional

_CHAVE = secrets.token_bytes(32)


class ErroCertificado(Exception):
    pass


def _selar(*partes) -> str:
    return hmac.new(_CHAVE, repr(partes).encode("utf-8"), hashlib.sha256).hexdigest()


def _exigir_chamador(modulo: str, funcoes: tuple) -> None:
    f = sys._getframe(2)
    if f.f_globals.get("__name__") != modulo or f.f_code.co_name not in funcoes:
        raise ErroCertificado(f"certificado só pode ser emitido por {modulo}.{'/'.join(funcoes)} "
                              f"(chamador: {f.f_globals.get('__name__')}.{f.f_code.co_name})")


@dataclass(frozen=True)
class CertificadoBusca:
    termo: tuple
    tipo: tuple
    tabela: str
    selo: str


@dataclass(frozen=True)
class CertificadoDescoberta:
    termo: tuple
    tarefa_id: str
    aprendiz_id: str
    indice_resultado: int
    busca: CertificadoBusca
    selo: str


@dataclass(frozen=True)
class CertificadoEntrada:
    nome: str
    corpo: tuple
    biblioteca_id: int
    selo: str


def emitir_busca(termo, tipo, tabela_nome: str) -> CertificadoBusca:
    _exigir_chamador("fedro_piloto.enumerador", ("buscar",))
    return CertificadoBusca(termo, tipo, tabela_nome, _selar("busca", termo, tipo, tabela_nome))


def busca_valida(c: Optional[CertificadoBusca]) -> bool:
    return (isinstance(c, CertificadoBusca)
            and hmac.compare_digest(c.selo, _selar("busca", c.termo, c.tipo, c.tabela)))


def emitir_descoberta(cb: CertificadoBusca, termo, tarefa_id: str, aprendiz_id: str,
                      indice_resultado: int) -> CertificadoDescoberta:
    _exigir_chamador("fedro_piloto.aprendizes", ("resolver",))
    if not busca_valida(cb) or cb.termo != termo:
        raise ErroCertificado("termo aceito sem certificado de busca válido para ele")
    return CertificadoDescoberta(termo, tarefa_id, aprendiz_id, indice_resultado, cb,
                                 _selar("descoberta", termo, tarefa_id, aprendiz_id, indice_resultado, cb.selo))


def descoberta_valida(c: Optional[CertificadoDescoberta], termo=None, tarefa_id: Optional[str] = None) -> bool:
    """Certificado íntegro; se termo/tarefa_id forem dados, também ligados a eles."""
    if not isinstance(c, CertificadoDescoberta) or not busca_valida(c.busca) or c.busca.termo != c.termo:
        return False
    if not hmac.compare_digest(c.selo, _selar("descoberta", c.termo, c.tarefa_id, c.aprendiz_id,
                                                c.indice_resultado, c.busca.selo)):
        return False
    if termo is not None and termo != c.termo:
        return False
    if tarefa_id is not None and tarefa_id != c.tarefa_id:
        return False
    return True


def emitir_entrada(nome: str, corpo, biblioteca_id: int) -> CertificadoEntrada:
    _exigir_chamador("fedro_piloto.biblioteca", ("adicionar",))
    return CertificadoEntrada(nome, corpo, biblioteca_id, _selar("entrada", nome, corpo, biblioteca_id))


def entrada_valida(c: Optional[CertificadoEntrada], nome: str, corpo) -> bool:
    return (isinstance(c, CertificadoEntrada) and c.nome == nome and c.corpo == corpo
            and hmac.compare_digest(c.selo, _selar("entrada", c.nome, c.corpo, c.biblioteca_id)))
