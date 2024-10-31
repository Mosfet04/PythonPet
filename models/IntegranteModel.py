# app/models/taskModel.py

from datetime import date
from typing import Optional
from peewee import Model, CharField, DateField, TextField, ForeignKeyField, IntegrityError, DoesNotExist, OperationalError
from dtos.requests.Integrante.UpdateIntegranteRequest import UpdateIntegranteRequest
from dtos.responses.IntegranteResponse import IntegranteResponse
from servicos.postegre import Postgre
from .SetorModel import Setor
from dtos.responses.PaginacaoResponse import PaginacaoResponse

# Configuração do banco de dados
db = Postgre.get_database()

class Integrante(Model):
    """
    Modelo do banco de Integrante.
    """
    nome = CharField()
    matricula = CharField()  
    email = CharField() 
    dataIngresso = DateField()  
    dataDesligamento = DateField(null = True) 
    linkSelfie = TextField()
    setor = ForeignKeyField(Setor, backref="integrantes", null=True)  

    def encontrarIntegrante(matricula: str, idIntegrante: int):
        try:
            if ((matricula is None or matricula == "") and idIntegrante is not None):
                return Integrante.select().where(Integrante.id == idIntegrante).first()
            elif(matricula is not None and matricula != ""):
                return Integrante.select().where(Integrante.matricula == matricula).first()
            else:
                print(f"Erro ao encontrar integrante: matrícula e idIntegrante são nulos")
                return None
        except Exception as e:
            print(f"Erro ao encontrar integrante com matrícula {matricula}: {e}")
            return None

    def criarIntegrante(nome: str, matricula: str, email: str, linkSelfie: str, setorId: int) -> IntegranteResponse:
        try:
            integranteCriado = Integrante.create(
                nome=nome,
                dataDesligamento=None,
                matricula=matricula,
                email=email,
                dataIngresso=date.today(),
                linkSelfie=linkSelfie,
                setor=setorId
            )

            return IntegranteResponse(
                id=integranteCriado.id,
                nome=integranteCriado.nome,
                dataDesligamento=str(integranteCriado.dataDesligamento),
                matricula=integranteCriado.matricula,
                email=integranteCriado.email,
                dataIngresso=str(integranteCriado.dataIngresso),
                linkSelfie=integranteCriado.linkSelfie,
                setorNome=integranteCriado.setor.nome
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao criar integrante: {e}")
            return None
    
    def listarIntegrantes(ativos: bool, page: int = 1, per_page: int = 10, 
        NonPaginated: Optional[bool] = False) -> PaginacaoResponse[IntegranteResponse]:
        try:
            query = Integrante.select()
            if ativos:
                query = query.where(Integrante.dataDesligamento == None)
            
            total_items = query.count()
            total_pages = (total_items +per_page - 1) // per_page

            if NonPaginated:
                return query.first()
            query = query.order_by(Integrante.dataIngresso)
            query = query.paginate(page, per_page)
            listaIntegrantes = query.execute()

            response_list = [
                IntegranteResponse(
                    id=integrante.id,
                    nome=integrante.nome,
                    dataDesligamento=str(integrante.dataDesligamento),
                    matricula=integrante.matricula,
                    email=integrante.email,
                    dataIngresso=str(integrante.dataIngresso),
                    linkSelfie=integrante.linkSelfie,
                    setorNome=integrante.setor.nome
                ).dict() for integrante in listaIntegrantes
            ]

            return PaginacaoResponse(
                hasNextPage=page < total_pages,
                page=page,
                totalPage=total_pages,
                qtdItens=total_items,
                items=response_list
            )
        except Exception as e:
            print(f"Erro inesperado ao listar integrantes: {e}")
            return PaginacaoResponse(hasNextPage=False, page=1, totalPage=1, qtdItens=0, items=[])

    def atualizarIntegrante(self, request: UpdateIntegranteRequest) -> IntegranteResponse:  
        try:
            self.nome = request.nome
            self.matricula = request.matricula
            self.email = request.email
            self.dataIngresso = request.dataIngresso
            self.dataDesligamento = date.today() if request.desligamento else None
            self.linkSelfie = request.linkSelfie
            self.setor = request.setorId

            self.save()

            return IntegranteResponse(
                id=self.id,
                nome=self.nome,
                dataDesligamento=str(self.dataDesligamento),
                matricula=self.matricula,
                email=self.email,
                dataIngresso=str(self.dataIngresso),
                linkSelfie=self.linkSelfie,
                setorNome=self.setor.nome
            ).dict()
        except IntegrityError as e:
            print(f"Erro ao atualizar integrante: {e}")
            return None

    def deletarIntegrante(self):
        try:
            self.delete_instance()
            return True
        except IntegrityError as e:
            print(f"Erro ao deletar integrante: {e}")
            return False
    class Meta:
        database = db
