import { Canvas } from "@react-three/fiber";
import { Float, OrbitControls } from "@react-three/drei";

function FloatingIcon({ position, color }) {
  return (
    <Float speed={2} rotationIntensity={2} floatIntensity={2}>
      <mesh position={position}>
        <sphereGeometry args={[0.3, 32, 32]} />
        <meshStandardMaterial color={color} />
      </mesh>
    </Float>
  );
}

export default function HeroScene() {
  return (
    <Canvas camera={{ position: [0, 0, 6] }}>
      <ambientLight intensity={1} />
      <directionalLight position={[5, 5, 5]} />

      {/* Floating objects representing features */}

      <FloatingIcon position={[-2, 1, 0]} color="#6366f1" />
      <FloatingIcon position={[2, 1, 0]} color="#ec4899" />
      <FloatingIcon position={[0, -1, 0]} color="#10b981" />

      <OrbitControls enableZoom={false} enablePan={false} />
    </Canvas>
  );
}