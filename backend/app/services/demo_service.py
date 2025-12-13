from sqlalchemy.orm import Session
from app.models.kpi import KPI
from app.models.user import User

def clean_demo_data(db: Session, user: User):
    """Elimina todos los datos creados por el usuario demo."""
    db.query(KPI).filter(KPI.created_by == user.id).delete()
    db.commit()

def seed_demo_data(db: Session, user: User):
    """Inserta datos originales para el usuario demo."""
    demo_kpis = [
        KPI(
            title="Ventas Mensuales",
            description="KPI demo de ventas",
            current_value=120,
            target_value=200,
            unit="USD",
            category="Ventas",
            created_by=user.id
        ),
        KPI(
            title="Clientes Nuevos",
            description="KPI demo de clientes",
            current_value=30,
            target_value=50,
            unit="Clientes",
            category="Clientes",
            created_by=user.id
        )
    ]

    db.add_all(demo_kpis)
    db.commit()
