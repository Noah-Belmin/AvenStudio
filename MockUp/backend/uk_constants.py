"""
UK Self-Build Constants
Standard phases, categories, and terminology for UK construction projects
"""

# UK Build Phases (Standard self-build sequence)
UK_BUILD_PHASES = [
    {
        'id': 'pre-planning',
        'name': 'Pre-Planning & Feasibility',
        'description': 'Initial site assessment, feasibility studies, and concept development',
        'typical_duration_weeks': 4,
        'order': 1
    },
    {
        'id': 'planning-application',
        'name': 'Planning Application',
        'description': 'Submitting and obtaining planning permission from local authority',
        'typical_duration_weeks': 12,
        'order': 2
    },
    {
        'id': 'building-regs',
        'name': 'Building Regulations',
        'description': 'Building control approval and compliance documentation',
        'typical_duration_weeks': 6,
        'order': 3
    },
    {
        'id': 'tender-procurement',
        'name': 'Tender & Procurement',
        'description': 'Contractor selection, quotes, and material procurement',
        'typical_duration_weeks': 4,
        'order': 4
    },
    {
        'id': 'site-setup',
        'name': 'Site Setup',
        'description': 'Site access, utilities connection, and temporary facilities',
        'typical_duration_weeks': 2,
        'order': 5
    },
    {
        'id': 'groundworks',
        'name': 'Groundworks & Foundations',
        'description': 'Excavation, foundations, drainage, and DPC',
        'typical_duration_weeks': 4,
        'order': 6
    },
    {
        'id': 'substructure',
        'name': 'Substructure',
        'description': 'Below ground-level construction and damp proofing',
        'typical_duration_weeks': 2,
        'order': 7
    },
    {
        'id': 'superstructure',
        'name': 'Superstructure',
        'description': 'Walls, roof structure, and external envelope',
        'typical_duration_weeks': 8,
        'order': 8
    },
    {
        'id': 'external-envelope',
        'name': 'External Envelope',
        'description': 'Windows, doors, external cladding, and weatherproofing',
        'typical_duration_weeks': 4,
        'order': 9
    },
    {
        'id': 'first-fix-carpentry',
        'name': 'First Fix Carpentry',
        'description': 'Stud walls, floor joists, roof timbers, and battens',
        'typical_duration_weeks': 3,
        'order': 10
    },
    {
        'id': 'first-fix-electrics',
        'name': 'First Fix Electrics',
        'description': 'Cable runs, back boxes, and consumer unit installation',
        'typical_duration_weeks': 2,
        'order': 11
    },
    {
        'id': 'first-fix-plumbing',
        'name': 'First Fix Plumbing & Heating',
        'description': 'Pipework, radiators, underfloor heating, and boiler installation',
        'typical_duration_weeks': 2,
        'order': 12
    },
    {
        'id': 'insulation',
        'name': 'Insulation',
        'description': 'Wall, floor, and roof insulation for thermal performance',
        'typical_duration_weeks': 2,
        'order': 13
    },
    {
        'id': 'plastering',
        'name': 'Plastering',
        'description': 'Plasterboard and skim finishing to walls and ceilings',
        'typical_duration_weeks': 3,
        'order': 14
    },
    {
        'id': 'second-fix-carpentry',
        'name': 'Second Fix Carpentry',
        'description': 'Skirting, architrave, doors, and fitted furniture',
        'typical_duration_weeks': 3,
        'order': 15
    },
    {
        'id': 'second-fix-electrics',
        'name': 'Second Fix Electrics',
        'description': 'Switches, sockets, light fittings, and testing',
        'typical_duration_weeks': 2,
        'order': 16
    },
    {
        'id': 'second-fix-plumbing',
        'name': 'Second Fix Plumbing',
        'description': 'Sanitaryware, taps, kitchen appliances, and commissioning',
        'typical_duration_weeks': 2,
        'order': 17
    },
    {
        'id': 'finishes',
        'name': 'Finishes & Decorating',
        'description': 'Painting, tiling, flooring, and final decorative touches',
        'typical_duration_weeks': 4,
        'order': 18
    },
    {
        'id': 'snagging',
        'name': 'Snagging & Handover',
        'description': 'Final inspections, defect fixing, and project completion',
        'typical_duration_weeks': 2,
        'order': 19
    }
]

# Budget Categories (Standard UK self-build)
UK_BUDGET_CATEGORIES = [
    {
        'id': 'land',
        'name': 'Land & Legal',
        'description': 'Land purchase, legal fees, stamp duty'
    },
    {
        'id': 'professional-fees',
        'name': 'Professional Fees',
        'description': 'Architect, structural engineer, surveyors, planning consultants'
    },
    {
        'id': 'groundworks',
        'name': 'Groundworks',
        'description': 'Excavation, foundations, drainage'
    },
    {
        'id': 'structure',
        'name': 'Structure',
        'description': 'Walls, roof, structural elements'
    },
    {
        'id': 'external-works',
        'name': 'External Works',
        'description': 'Landscaping, driveway, boundary walls'
    },
    {
        'id': 'mep',
        'name': 'M&E (Mechanical & Electrical)',
        'description': 'Plumbing, heating, electrics, renewables'
    },
    {
        'id': 'finishes',
        'name': 'Finishes',
        'description': 'Flooring, tiling, painting, decorating'
    },
    {
        'id': 'kitchen-bathrooms',
        'name': 'Kitchen & Bathrooms',
        'description': 'Fitted kitchens, bathroom suites, sanitaryware'
    },
    {
        'id': 'contingency',
        'name': 'Contingency',
        'description': 'Reserve fund for unforeseen costs (typically 10-15%)'
    }
]

# Building Regulations Parts (UK)
UK_BUILDING_REGS_PARTS = {
    'A': 'Structure',
    'B': 'Fire Safety',
    'C': 'Site Preparation & Resistance to Contaminants & Moisture',
    'D': 'Toxic Substances',
    'E': 'Resistance to the Passage of Sound',
    'F': 'Ventilation',
    'G': 'Sanitation, Hot Water Safety & Water Efficiency',
    'H': 'Drainage & Waste Disposal',
    'J': 'Combustion Appliances & Fuel Storage Systems',
    'K': 'Protection from Falling, Collision & Impact',
    'L': 'Conservation of Fuel & Power (Energy Efficiency)',
    'M': 'Access to & Use of Buildings',
    'N': 'Glazing - Safety in Relation to Impact, Opening & Cleaning',
    'O': 'Overheating',
    'P': 'Electrical Safety',
    'Q': 'Security',
    'R': 'Physical Infrastructure for High-Speed Electronic Communications'
}

# Common Contact Roles (UK construction)
UK_CONTACT_ROLES = [
    'Architect',
    'Structural Engineer',
    'M&E Engineer',
    'Quantity Surveyor',
    'Main Contractor',
    'Project Manager',
    'Builder',
    'Groundworker',
    'Bricklayer',
    'Roofer',
    'Carpenter',
    'Electrician',
    'Plumber',
    'Plasterer',
    'Decorator',
    'Landscaper',
    'Building Control Officer',
    'Planning Consultant',
    'Supplier',
    'Other'
]

# Document Types (UK self-build)
UK_DOCUMENT_TYPES = {
    'planning': 'Planning Permission',
    'building_regs': 'Building Regulations',
    'certificate': 'Certificates & Warranties',
    'drawing': 'Drawings & Plans',
    'contract': 'Contracts',
    'invoice': 'Invoices & Receipts',
    'photo': 'Site Photos',
    'sap': 'SAP Calculations',
    'warranty': 'Warranties',
    'insurance': 'Insurance Documents',
    'other': 'Other'
}

# Material Units (UK construction)
UK_MATERIAL_UNITS = [
    'm²',      # Square metres
    'm³',      # Cubic metres
    'linear m', # Linear metres
    'tonnes',
    'kg',
    'units',
    'bags',
    'litres',
    'rolls',
    'sheets',
    'blocks',
    'bricks',
    'other'
]

def get_phase_by_id(phase_id: str) -> dict:
    """Get phase details by ID"""
    return next((p for p in UK_BUILD_PHASES if p['id'] == phase_id), None)

def get_phase_order(phase_id: str) -> int:
    """Get phase order number"""
    phase = get_phase_by_id(phase_id)
    return phase['order'] if phase else 999

def get_all_phase_ids() -> list:
    """Get list of all phase IDs"""
    return [p['id'] for p in UK_BUILD_PHASES]

def get_all_phase_names() -> list:
    """Get list of all phase names"""
    return [p['name'] for p in UK_BUILD_PHASES]

def estimate_project_duration_weeks() -> int:
    """Estimate total project duration based on typical phase durations"""
    return sum(p['typical_duration_weeks'] for p in UK_BUILD_PHASES)
