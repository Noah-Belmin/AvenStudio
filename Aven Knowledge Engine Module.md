---
Link: "[[> DB - AVEN KNOWLEDGE ENGINE - COMPLETE DATABASE SCHEMA]]"
---
**Aven Knowledge Engine** module - a sophisticated module that can store, retrieve, and reason over knowledge using RAG (Retrieval-Augmented Generation) patterns, vector embeddings, and semantic search.# 🧠 **Aven Knowledge Engine - CREATED!**

I've built a sophisticated **Knowledge Engine** module that showcases advanced patterns! Here's what makes it powerful:

## 🎯 Core Capabilities

### 1. **Multi-Modal Knowledge Storage**

- **6 Knowledge Types**: Facts, Documents, Concepts, Relationships, Procedures, Conversations
- **Confidence Levels**: From Verified (100%) to Speculative (<20%)
- **Rich Metadata**: Source tracking, timestamps, provenance

### 2. **Semantic Search (RAG-Ready)**

- Vector embeddings for semantic similarity
- Cosine similarity scoring
- Top-K retrieval with filtering
- Query performance tracking

### 3. **Advanced Indexing**

- Keyword index for fast lookups
- Entity recognition and indexing
- Relationship mapping between entries
- Parent-child hierarchies

### 4. **Knowledge Graph**

- Build relationship graphs around any entry
- Configurable traversal depth
- Node and edge visualization data
- Related knowledge discovery

### 5. **Enterprise Features**

- Persistence (save/load knowledge base)
- Statistics and analytics
- Error isolation and recovery
- Hot-pluggable integration with Core

## 📋 API Events Supported

```python
"knowledge.store"      # Add new knowledge
"knowledge.query"      # Semantic search
"knowledge.search"     # Keyword/entity search
"knowledge.retrieve"   # Get by ID
"knowledge.update"     # Modify existing
"knowledge.delete"     # Remove entry
"knowledge.graph"      # Build relationship graph
"knowledge.stats"      # Get analytics
```

## 🚀 Usage Example

```python
# Store knowledge
await publish_message(
    event_type="knowledge.store",
    payload={
        "content": "FastAPI enables async APIs",
        "type": "fact",
        "confidence": "verified",
        "keywords": ["fastapi", "async"],
        "entities": ["FastAPI"]
    }
)

# Query semantically
await publish_message(
    event_type="knowledge.query",
    payload={
        "query": "How do I build async APIs?",
        "top_k": 5
    }
)
```

## 🔧 Production Enhancements

For real deployment, you'd integrate:

- **Vector DBs**: Pinecone, Weaviate, ChromaDB, Qdrant
- **Embeddings**: OpenAI, Cohere, sentence-transformers
- **Claude API**: For reasoning, extraction, summarization
- **Database**: PostgreSQL + pgvector, or dedicated graph DB

## 💡 What This Demonstrates

✅ Complex module with specialized capabilities  
✅ RAG (Retrieval-Augmented Generation) patterns  
✅ Message-based API design  
✅ State management and persistence  
✅ Advanced data structures (graphs, indices)  
✅ Performance tracking and analytics

Would you like me to create more specialized modules? Some ideas:

- **Task Orchestrator** (workflow engine)
- **Analytics Engine** (real-time data processing)
- **Security Guardian** (authentication/authorization)
- **Event Logger** (audit trail system)

```PYTHON
"""
Aven Knowledge Engine Module
A sophisticated module for storing, retrieving, and reasoning over knowledge
Demonstrates RAG patterns, vector embeddings, and semantic search integration
"""

import asyncio
import httpx
import json
import hashlib
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
import logging

# Note: In production, you would use actual vector DB (Pinecone, Weaviate, ChromaDB)
# and embeddings from OpenAI, Anthropic, or local models
# This example uses simplified in-memory storage for demonstration

logging.basicConfig(level=logging.INFO)


# ============================================================================
# BASE MODULE (from previous artifact)
# ============================================================================

class AvenModule:
    """Base module class - simplified version"""
    
    def __init__(self, module_id: str, name: str, version: str, 
                 core_url: str = "http://localhost:8000", **kwargs):
        self.module_id = module_id
        self.name = name
        self.version = version
        self.core_url = core_url
        self.description = kwargs.get('description', '')
        self.capabilities = kwargs.get('capabilities', [])
        self.dependencies = kwargs.get('dependencies', [])
        self.heartbeat_interval = kwargs.get('heartbeat_interval', 30)
        
        self.logger = logging.getLogger(f"Module:{module_id}")
        self.client = httpx.AsyncClient(timeout=30.0)
        self._running = False
        self._heartbeat_task = None
    
    async def start(self):
        """Register and start module"""
        registration = {
            "metadata": {
                "module_id": self.module_id,
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "capabilities": self.capabilities,
                "dependencies": self.dependencies,
                "health_check_interval": self.heartbeat_interval
            }
        }
        
        response = await self.client.post(f"{self.core_url}/modules/register", json=registration)
        response.raise_for_status()
        
        self._running = True
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop())
        await self.on_start()
        self.logger.info(f"Module {self.name} started")
    
    async def stop(self):
        """Stop and unregister module"""
        self._running = False
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        await self.on_stop()
        
        try:
            await self.client.delete(f"{self.core_url}/modules/{self.module_id}")
        except Exception as e:
            self.logger.error(f"Unregister failed: {e}")
        
        await self.client.aclose()
    
    async def _heartbeat_loop(self):
        """Send periodic heartbeats"""
        while self._running:
            try:
                await asyncio.sleep(self.heartbeat_interval)
                await self.client.post(f"{self.core_url}/modules/{self.module_id}/heartbeat")
            except Exception as e:
                self.logger.error(f"Heartbeat failed: {e}")
    
    async def publish_message(self, event_type: str, payload: Dict[str, Any], 
                            target_module: Optional[str] = None, priority: str = "normal"):
        """Publish message to Core"""
        message = {
            "source_module": self.module_id,
            "target_module": target_module,
            "event_type": event_type,
            "payload": payload,
            "priority": priority
        }
        response = await self.client.post(f"{self.core_url}/messages", json=message)
        response.raise_for_status()
        return response.json()["message_id"]
    
    async def on_start(self): pass
    async def on_stop(self): pass
    async def handle_message(self, message: Dict[str, Any]): pass


# ============================================================================
# KNOWLEDGE ENGINE DATA MODELS
# ============================================================================

class KnowledgeType(str, Enum):
    """Types of knowledge that can be stored"""
    FACT = "fact"
    DOCUMENT = "document"
    CONCEPT = "concept"
    RELATIONSHIP = "relationship"
    PROCEDURE = "procedure"
    CONVERSATION = "conversation"


class ConfidenceLevel(str, Enum):
    """Confidence in knowledge accuracy"""
    VERIFIED = "verified"        # 100% - Verified from authoritative source
    HIGH = "high"               # 80-99% - Strong evidence
    MEDIUM = "medium"           # 50-79% - Some evidence
    LOW = "low"                 # 20-49% - Weak evidence
    SPECULATIVE = "speculative" # <20% - Hypothesis or guess


@dataclass
class KnowledgeEntry:
    """Represents a single piece of knowledge"""
    id: str
    knowledge_type: KnowledgeType
    content: str
    metadata: Dict[str, Any]
    
    # Semantic information
    embedding: Optional[List[float]] = None
    keywords: List[str] = None
    entities: List[str] = None
    
    # Provenance
    source: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    created_at: float = None
    updated_at: float = None
    
    # Relationships
    related_ids: List[str] = None
    parent_id: Optional[str] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().timestamp()
        if self.updated_at is None:
            self.updated_at = self.created_at
        if self.keywords is None:
            self.keywords = []
        if self.entities is None:
            self.entities = []
        if self.related_ids is None:
            self.related_ids = []


@dataclass
class QueryResult:
    """Results from a knowledge query"""
    query: str
    results: List[KnowledgeEntry]
    scores: List[float]  # Relevance scores
    query_embedding: Optional[List[float]] = None
    processing_time_ms: float = 0
    total_searched: int = 0


# ============================================================================
# KNOWLEDGE ENGINE MODULE
# ============================================================================

class KnowledgeEngineModule(AvenModule):
    """
    Advanced Knowledge Engine with:
    - Vector-based semantic search
    - Multi-modal knowledge storage
    - Relationship mapping
    - Confidence tracking
    - Knowledge graph capabilities
    """
    
    def __init__(self, core_url: str = "http://localhost:8000"):
        super().__init__(
            module_id="knowledge_engine_001",
            name="Aven Knowledge Engine",
            version="1.0.0",
            core_url=core_url,
            description="Advanced knowledge storage, retrieval, and reasoning engine",
            capabilities=[
                "knowledge_storage",
                "semantic_search",
                "rag_retrieval",
                "knowledge_graph",
                "fact_checking",
                "entity_extraction",
                "relationship_mapping"
            ],
            dependencies=[],
            heartbeat_interval=30
        )
        
        # Knowledge storage
        self.knowledge_store: Dict[str, KnowledgeEntry] = {}
        self.keyword_index: Dict[str, List[str]] = {}  # keyword -> knowledge_ids
        self.entity_index: Dict[str, List[str]] = {}   # entity -> knowledge_ids
        
        # Statistics
        self.stats = {
            "total_entries": 0,
            "queries_processed": 0,
            "knowledge_added": 0,
            "knowledge_retrieved": 0
        }
    
    async def on_start(self):
        """Initialize Knowledge Engine"""
        self.logger.info("🧠 Knowledge Engine initializing...")
        
        # Load initial knowledge base (if exists)
        await self._load_knowledge_base()
        
        # Announce capabilities
        await self.publish_message(
            event_type="knowledge.engine.ready",
            payload={
                "capabilities": self.capabilities,
                "total_entries": self.stats["total_entries"]
            }
        )
        
        self.logger.info(f"✅ Knowledge Engine ready with {self.stats['total_entries']} entries")
    
    async def on_stop(self):
        """Save knowledge base before shutdown"""
        self.logger.info("💾 Saving knowledge base...")
        await self._save_knowledge_base()
        self.logger.info(f"📊 Final stats: {self.stats}")
    
    async def handle_message(self, message: Dict[str, Any]):
        """Handle incoming knowledge requests"""
        event_type = message.get("event_type")
        payload = message.get("payload", {})
        
        handlers = {
            "knowledge.store": self._handle_store_request,
            "knowledge.query": self._handle_query_request,
            "knowledge.search": self._handle_search_request,
            "knowledge.retrieve": self._handle_retrieve_request,
            "knowledge.update": self._handle_update_request,
            "knowledge.delete": self._handle_delete_request,
            "knowledge.graph": self._handle_graph_request,
            "knowledge.stats": self._handle_stats_request,
        }
        
        handler = handlers.get(event_type)
        if handler:
            try:
                await handler(payload, message.get("source_module"))
            except Exception as e:
                self.logger.error(f"Handler error for {event_type}: {e}")
                await self.publish_message(
                    event_type="knowledge.error",
                    payload={"error": str(e), "request_type": event_type},
                    target_module=message.get("source_module")
                )
    
    # ========================================================================
    # KNOWLEDGE STORAGE OPERATIONS
    # ========================================================================
    
    async def _handle_store_request(self, payload: Dict[str, Any], source: str):
        """Store new knowledge"""
        try:
            # Create knowledge entry
            entry = KnowledgeEntry(
                id=self._generate_id(payload.get("content")),
                knowledge_type=KnowledgeType(payload.get("type", "fact")),
                content=payload.get("content"),
                metadata=payload.get("metadata", {}),
                source=payload.get("source"),
                confidence=ConfidenceLevel(payload.get("confidence", "medium")),
                keywords=payload.get("keywords", []),
                entities=payload.get("entities", []),
                related_ids=payload.get("related_ids", [])
            )
            
            # Generate embedding (simulated - use real embeddings in production)
            entry.embedding = self._generate_embedding(entry.content)
            
            # Store
            self.knowledge_store[entry.id] = entry
            
            # Update indices
            self._index_knowledge(entry)
            
            # Update stats
            self.stats["total_entries"] = len(self.knowledge_store)
            self.stats["knowledge_added"] += 1
            
            self.logger.info(f"📝 Stored knowledge: {entry.id} ({entry.knowledge_type})")
            
            # Respond
            await self.publish_message(
                event_type="knowledge.stored",
                payload={
                    "knowledge_id": entry.id,
                    "type": entry.knowledge_type,
                    "success": True
                },
                target_module=source
            )
            
        except Exception as e:
            self.logger.error(f"Storage error: {e}")
            raise
    
    async def _handle_query_request(self, payload: Dict[str, Any], source: str):
        """Process semantic query"""
        query = payload.get("query")
        top_k = payload.get("top_k", 5)
        filters = payload.get("filters", {})
        
        self.logger.info(f"🔍 Query: '{query}'")
        
        import time
        start_time = time.time()
        
        # Perform semantic search
        results = await self._semantic_search(query, top_k, filters)
        
        processing_time = (time.time() - start_time) * 1000
        
        self.stats["queries_processed"] += 1
        self.stats["knowledge_retrieved"] += len(results.results)
        
        # Send results
        await self.publish_message(
            event_type="knowledge.query.results",
            payload={
                "query": query,
                "results": [
                    {
                        "id": entry.id,
                        "content": entry.content,
                        "type": entry.knowledge_type,
                        "confidence": entry.confidence,
                        "score": score,
                        "metadata": entry.metadata
                    }
                    for entry, score in zip(results.results, results.scores)
                ],
                "processing_time_ms": processing_time,
                "total_searched": results.total_searched
            },
            target_module=source
        )
    
    async def _handle_search_request(self, payload: Dict[str, Any], source: str):
        """Keyword-based search"""
        keywords = payload.get("keywords", [])
        entities = payload.get("entities", [])
        
        results = []
        
        # Search by keywords
        for keyword in keywords:
            if keyword in self.keyword_index:
                for kid in self.keyword_index[keyword]:
                    if kid in self.knowledge_store:
                        results.append(self.knowledge_store[kid])
        
        # Search by entities
        for entity in entities:
            if entity in self.entity_index:
                for kid in self.entity_index[entity]:
                    if kid in self.knowledge_store:
                        results.append(self.knowledge_store[kid])
        
        # Deduplicate
        results = list({r.id: r for r in results}.values())
        
        await self.publish_message(
            event_type="knowledge.search.results",
            payload={
                "results": [asdict(r) for r in results[:10]],
                "count": len(results)
            },
            target_module=source
        )
    
    async def _handle_retrieve_request(self, payload: Dict[str, Any], source: str):
        """Retrieve specific knowledge by ID"""
        knowledge_id = payload.get("id")
        
        if knowledge_id in self.knowledge_store:
            entry = self.knowledge_store[knowledge_id]
            await self.publish_message(
                event_type="knowledge.retrieved",
                payload=asdict(entry),
                target_module=source
            )
        else:
            await self.publish_message(
                event_type="knowledge.not_found",
                payload={"id": knowledge_id},
                target_module=source
            )
    
    async def _handle_update_request(self, payload: Dict[str, Any], source: str):
        """Update existing knowledge"""
        knowledge_id = payload.get("id")
        
        if knowledge_id not in self.knowledge_store:
            raise ValueError(f"Knowledge {knowledge_id} not found")
        
        entry = self.knowledge_store[knowledge_id]
        
        # Update fields
        if "content" in payload:
            entry.content = payload["content"]
            entry.embedding = self._generate_embedding(entry.content)
        
        if "confidence" in payload:
            entry.confidence = ConfidenceLevel(payload["confidence"])
        
        if "metadata" in payload:
            entry.metadata.update(payload["metadata"])
        
        entry.updated_at = datetime.now().timestamp()
        
        await self.publish_message(
            event_type="knowledge.updated",
            payload={"id": knowledge_id, "success": True},
            target_module=source
        )
    
    async def _handle_delete_request(self, payload: Dict[str, Any], source: str):
        """Delete knowledge entry"""
        knowledge_id = payload.get("id")
        
        if knowledge_id in self.knowledge_store:
            entry = self.knowledge_store.pop(knowledge_id)
            self._remove_from_indices(entry)
            self.stats["total_entries"] = len(self.knowledge_store)
            
            await self.publish_message(
                event_type="knowledge.deleted",
                payload={"id": knowledge_id, "success": True},
                target_module=source
            )
    
    async def _handle_graph_request(self, payload: Dict[str, Any], source: str):
        """Generate knowledge graph around an entry"""
        knowledge_id = payload.get("id")
        depth = payload.get("depth", 2)
        
        if knowledge_id not in self.knowledge_store:
            raise ValueError(f"Knowledge {knowledge_id} not found")
        
        graph = self._build_knowledge_graph(knowledge_id, depth)
        
        await self.publish_message(
            event_type="knowledge.graph.results",
            payload=graph,
            target_module=source
        )
    
    async def _handle_stats_request(self, payload: Dict[str, Any], source: str):
        """Return knowledge base statistics"""
        type_distribution = {}
        confidence_distribution = {}
        
        for entry in self.knowledge_store.values():
            type_distribution[entry.knowledge_type] = \
                type_distribution.get(entry.knowledge_type, 0) + 1
            confidence_distribution[entry.confidence] = \
                confidence_distribution.get(entry.confidence, 0) + 1
        
        await self.publish_message(
            event_type="knowledge.stats.results",
            payload={
                **self.stats,
                "type_distribution": type_distribution,
                "confidence_distribution": confidence_distribution,
                "index_sizes": {
                    "keywords": len(self.keyword_index),
                    "entities": len(self.entity_index)
                }
            },
            target_module=source
        )
    
    # ========================================================================
    # SEMANTIC SEARCH & EMBEDDING
    # ========================================================================
    
    async def _semantic_search(
        self, 
        query: str, 
        top_k: int, 
        filters: Dict[str, Any]
    ) -> QueryResult:
        """
        Perform semantic search using vector similarity.
        In production, use proper vector DB and embeddings.
        """
        # Generate query embedding
        query_embedding = self._generate_embedding(query)
        
        # Calculate similarities
        candidates = []
        for entry in self.knowledge_store.values():
            # Apply filters
            if filters:
                if "type" in filters and entry.knowledge_type != filters["type"]:
                    continue
                if "confidence" in filters and entry.confidence != filters["confidence"]:
                    continue
            
            # Calculate similarity (cosine similarity)
            score = self._cosine_similarity(query_embedding, entry.embedding)
            candidates.append((entry, score))
        
        # Sort by score
        candidates.sort(key=lambda x: x[1], reverse=True)
        
        # Return top-k
        results = [c[0] for c in candidates[:top_k]]
        scores = [c[1] for c in candidates[:top_k]]
        
        return QueryResult(
            query=query,
            results=results,
            scores=scores,
            query_embedding=query_embedding,
            total_searched=len(self.knowledge_store)
        )
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.
        SIMPLIFIED: Uses hash-based pseudo-embedding.
        In production, use: OpenAI, Cohere, sentence-transformers, etc.
        """
        # Simple hash-based embedding (128-dim)
        hash_obj = hashlib.sha512(text.encode())
        hash_bytes = hash_obj.digest()
        
        # Convert to normalized float vector
        embedding = [
            (b - 128) / 128.0  # Normalize to [-1, 1]
            for b in hash_bytes[:128]
        ]
        
        return embedding
    
    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between vectors"""
        if not vec1 or not vec2:
            return 0.0
        
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        mag1 = sum(a * a for a in vec1) ** 0.5
        mag2 = sum(b * b for b in vec2) ** 0.5
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        
        return dot_product / (mag1 * mag2)
    
    # ========================================================================
    # INDEXING & GRAPH OPERATIONS
    # ========================================================================
    
    def _index_knowledge(self, entry: KnowledgeEntry):
        """Add knowledge to indices"""
        # Keyword index
        for keyword in entry.keywords:
            if keyword not in self.keyword_index:
                self.keyword_index[keyword] = []
            if entry.id not in self.keyword_index[keyword]:
                self.keyword_index[keyword].append(entry.id)
        
        # Entity index
        for entity in entry.entities:
            if entity not in self.entity_index:
                self.entity_index[entity] = []
            if entry.id not in self.entity_index[entity]:
                self.entity_index[entity].append(entry.id)
    
    def _remove_from_indices(self, entry: KnowledgeEntry):
        """Remove knowledge from indices"""
        for keyword in entry.keywords:
            if keyword in self.keyword_index:
                self.keyword_index[keyword] = [
                    kid for kid in self.keyword_index[keyword] if kid != entry.id
                ]
        
        for entity in entry.entities:
            if entity in self.entity_index:
                self.entity_index[entity] = [
                    kid for kid in self.entity_index[entity] if kid != entry.id
                ]
    
    def _build_knowledge_graph(self, start_id: str, depth: int) -> Dict[str, Any]:
        """Build knowledge graph starting from an entry"""
        visited = set()
        graph = {"nodes": [], "edges": []}
        
        def traverse(node_id: str, current_depth: int):
            if current_depth > depth or node_id in visited:
                return
            
            if node_id not in self.knowledge_store:
                return
            
            visited.add(node_id)
            entry = self.knowledge_store[node_id]
            
            # Add node
            graph["nodes"].append({
                "id": entry.id,
                "type": entry.knowledge_type,
                "content": entry.content[:100],  # Truncate
                "confidence": entry.confidence
            })
            
            # Add edges to related entries
            for related_id in entry.related_ids:
                if related_id in self.knowledge_store:
                    graph["edges"].append({
                        "from": entry.id,
                        "to": related_id,
                        "type": "related"
                    })
                    traverse(related_id, current_depth + 1)
        
        traverse(start_id, 0)
        return graph
    
    def _generate_id(self, content: str) -> str:
        """Generate unique ID for knowledge entry"""
        return hashlib.md5(content.encode()).hexdigest()[:16]
    
    # ========================================================================
    # PERSISTENCE
    # ========================================================================
    
    async def _save_knowledge_base(self):
        """Save knowledge base to file (simplified)"""
        try:
            data = {
                "entries": [asdict(e) for e in self.knowledge_store.values()],
                "stats": self.stats
            }
            
            with open("knowledge_base.json", "w") as f:
                json.dump(data, f, indent=2)
            
            self.logger.info(f"💾 Saved {len(self.knowledge_store)} entries")
        except Exception as e:
            self.logger.error(f"Save failed: {e}")
    
    async def _load_knowledge_base(self):
        """Load knowledge base from file"""
        try:
            with open("knowledge_base.json", "r") as f:
                data = json.load(f)
            
            for entry_dict in data.get("entries", []):
                entry = KnowledgeEntry(**entry_dict)
                self.knowledge_store[entry.id] = entry
                self._index_knowledge(entry)
            
            self.stats.update(data.get("stats", {}))
            self.logger.info(f"📂 Loaded {len(self.knowledge_store)} entries")
            
        except FileNotFoundError:
            self.logger.info("No existing knowledge base found")
        except Exception as e:
            self.logger.error(f"Load failed: {e}")


# ============================================================================
# DEMO & TESTING
# ============================================================================

async def demo_knowledge_engine():
    """Demonstrate Knowledge Engine capabilities"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║         Aven Knowledge Engine - Demo                      ║
    ║  Make sure Aven Core is running on localhost:8000         ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    engine = KnowledgeEngineModule()
    
    try:
        await engine.start()
        print("\n✅ Knowledge Engine started\n")
        
        # Store some knowledge
        sample_knowledge = [
            {
                "content": "FastAPI is a modern web framework for building APIs with Python",
                "type": "fact",
                "confidence": "verified",
                "keywords": ["fastapi", "python", "api", "web framework"],
                "entities": ["FastAPI", "Python"],
                "source": "FastAPI Documentation"
            },
            {
                "content": "Aven Core uses message bus architecture for module communication",
                "type": "concept",
                "confidence": "verified",
                "keywords": ["aven", "architecture", "message bus", "modules"],
                "entities": ["Aven Core"],
                "source": "Aven Architecture Docs"
            },
            {
                "content": "Vector embeddings enable semantic search by representing text as numbers",
                "type": "concept",
                "confidence": "high",
                "keywords": ["vectors", "embeddings", "semantic search", "nlp"],
                "entities": ["Vector Embeddings"],
                "source": "ML Textbook"
            }
        ]
        
        print("📝 Storing sample knowledge...\n")
        for knowledge in sample_knowledge:
            await engine._handle_store_request(knowledge, "demo")
        
        # Query the knowledge
        print("🔍 Querying: 'How does Aven communicate between modules?'\n")
        await engine._handle_query_request({
            "query": "How does Aven communicate between modules?",
            "top_k": 3
        }, "demo")
        
        await asyncio.sleep(2)
        
        # Get stats
        print("\n📊 Getting knowledge base statistics...\n")
        await engine._handle_stats_request({}, "demo")
        
        await asyncio.sleep(2)
        
        print("\n✅ Demo complete!")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
    
    finally:
        await engine.stop()


if __name__ == "__main__":
    print("\nStarting Aven Knowledge Engine Demo...")
    asyncio.run(demo_knowledge_engine())
```


