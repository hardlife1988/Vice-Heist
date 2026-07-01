"""
Deployment guide for Vice-heist slot game.

This document provides instructions for deploying Vice-heist
to production and integrating with StakeEngine.
"""

# DEPLOYMENT GUIDE

## Prerequisites

- Python 3.12+
- Node.js 24+ (for frontend)
- Docker (optional, for containerization)
- Rust (for performance-critical components)
- StakeEngine API credentials

## Phase 1: Local Testing

### 1. Run Unit Tests

```bash
python run_tests.py
```

Expected output:
- ✅ 20+ tests passing
- All game mechanics verified
- RTP calculations validated

### 2. Run Demo Game

```bash
cd math
python -c "from game_config import GameConfig; from ui import GameSimulator; config = GameConfig(); sim = GameSimulator(config, from gamestate import GameState; GameState(config)); sim.run_demo(10, 1.0)"
```

## Phase 2: Backend Setup

### 1. API Server

Create `api/server.py`:

```python
from flask import Flask, jsonify
from math.game_config import GameConfig
from math.reel_engine import ReelEngine
from math.win_evaluator import WinEvaluator
from math.gamestate import GameState

app = Flask(__name__)

@app.route('/api/game/spin', methods=['POST'])
def spin():
    # Handle spin request
    pass

@app.route('/api/game/config', methods=['GET'])
def get_config():
    config = GameConfig()
    return jsonify(config.__dict__)

if __name__ == '__main__':
    app.run(debug=False, port=5000)
```

### 2. Database Setup

```bash
# Create game sessions table
CREATE TABLE game_sessions (
    id UUID PRIMARY KEY,
    player_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    total_spins INT DEFAULT 0,
    total_wagered DECIMAL(10,2) DEFAULT 0,
    total_won DECIMAL(10,2) DEFAULT 0,
    final_balance DECIMAL(10,2) DEFAULT 0
);

# Create spins table
CREATE TABLE spins (
    id UUID PRIMARY KEY,
    session_id UUID REFERENCES game_sessions(id),
    spin_number INT,
    reel_grid JSONB,
    win_amount DECIMAL(10,2),
    features_triggered JSONB,
    verification_hash VARCHAR(256),
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. StakeEngine Integration

```python
from math.stake_engine import StakeEngineIntegration

# Initialize
stake_engine = StakeEngineIntegration(
    game_id="vice-heist-mainnet",
    api_key=os.getenv("STAKE_ENGINE_API_KEY")
)

# Generate server seed
server_seed_hash = stake_engine.generate_server_seed()

# Set client seed (from user)
stake_engine.set_client_seed(user_provided_seed)

# On each spin, generate fair spin
fair_spin = stake_engine.generate_provably_fair_spin(reel_grid)
```

## Phase 3: Frontend Setup

### 1. Web UI (React)

```bash
npx create-react-app frontend
cd frontend
npm install
```

### 2. Game Component

```typescript
// src/Game.tsx
import React from 'react';
import { GameUI } from './components/GameUI';
import { useGameState } from './hooks/useGameState';

export const Game: React.FC = () => {
  const { spin, gameState } = useGameState();
  
  return (
    <GameUI 
      onSpin={spin}
      gameState={gameState}
    />
  );
};
```

## Phase 4: Docker Containerization

### 1. Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "run_tests.py"]
```

### 2. Build & Run

```bash
docker build -t vice-heist:latest .
docker run -p 5000:5000 vice-heist:latest
```

## Phase 5: Production Deployment

### 1. Environment Variables

```bash
STAKE_ENGINE_API_KEY=<your-api-key>
DATABASE_URL=<production-db-url>
JWT_SECRET=<jwt-secret>
ALLOWED_ORIGINS=https://yourdomain.com
```

### 2. Deploy to Vercel/AWS

```bash
# Vercel
vercel deploy

# AWS Lambda
aws lambda create-function \
  --function-name vice-heist-api \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT:role/ROLE_NAME \
  --handler app.lambda_handler \
  --zip-file fileb://deployment.zip
```

## Phase 6: Monitoring & Analytics

### 1. Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
```

### 2. Metrics

- Track total spins per hour
- Monitor RTP vs theoretical
- Alert on anomalies (>5% variance)
- Track player retention
- Revenue per player

## Testing Checklist

- [ ] Unit tests pass (20+ tests)
- [ ] Integration tests pass
- [ ] RTP validates to ±2% over 100k spins
- [ ] Free spins trigger correctly
- [ ] Provably fair verification works
- [ ] API endpoints respond <200ms
- [ ] Database queries optimized
- [ ] UI responsive on mobile
- [ ] Security audit passed
- [ ] Legal compliance verified

## Security Considerations

1. **Input Validation** - Validate all bet amounts, game parameters
2. **Rate Limiting** - 100 spins/minute per player max
3. **JWT Auth** - Secure player sessions
4. **HTTPS Only** - All API calls encrypted
5. **Seed Verification** - Cryptographic validation of spins
6. **Audit Logging** - Log all game state changes

## Support & Troubleshooting

### RTP Not Matching

Run diagnostics:
```bash
python -c "from tests.test_game import *; unittest.main()"
```

### Performance Issues

- Profile with: `python -m cProfile app.py`
- Optimize database queries
- Enable caching for game config

### Deployment Fails

- Check requirements.txt versions
- Verify environment variables
- Review logs: `docker logs vice-heist`

## Next Steps

1. ✅ Run tests
2. ✅ Deploy backend
3. ✅ Build frontend
4. ✅ Integrate StakeEngine
5. ✅ Security audit
6. ✅ Launch beta
7. ✅ Gather feedback
8. ✅ Production launch

---

**For questions or issues, contact the development team.**
