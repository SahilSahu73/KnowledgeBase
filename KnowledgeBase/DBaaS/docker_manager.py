import os
import docker
from typing import Dict, Optional, Tuple
import yaml

class DockerManager:
    """Manages Docker containers for database instances"""
    
    def __init__(self):
        try:
            self.client = docker.from_env()
            self.client.ping()
        except Exception as e:
            raise Exception(f"Failed to connect to Docker: {e}")
    
    def create_container(self, instance_id: str, compose_file: str) -> Tuple[bool, str]:
        """Create and start a container using docker-compose configuration"""
        try:
            # Read docker-compose file
            with open(compose_file, 'r') as f:
                compose_config = yaml.safe_load(f)
            
            service_name = list(compose_config['services'].keys())[0]
            service_config = compose_config['services'][service_name]
            
            # Extract configuration
            container_config = {
                'name': f"{instance_id}",
                'image': service_config['image'],
                'environment': service_config.get('environment', {}),
                'ports': self._parse_ports(service_config.get('ports', [])),
                'volumes': self._parse_volumes(service_config.get('volumes', [])),
                'detach': True,
                'restart_policy': {"Name": service_config.get('restart', 'unless-stopped')},
                'mem_limit': service_config.get('mem_limit'),
                'cpu_quota': int(float(service_config.get('cpus', 1.0)) * 100000),
                'cpu_period': 100000,
                'network_mode': service_config.get('network_mode', 'bridge')
            }
            
            # Create container
            container = self.client.containers.run(**container_config)
            
            return True, f"Container {instance_id} created successfully"
        except docker.errors.ContainerError as e: # type: ignore
            return False, f"Container error: {e}"
        except docker.errors.ImageNotFound as e: # type: ignore
            return False, f"Image not found: {e}"
        except Exception as e:
            return False, f"Error creating container: {e}"
    
    def _parse_ports(self, ports: list) -> Dict:
        """Parse port mappings from docker-compose format"""
        port_dict = {}
        for port in ports:
            if isinstance(port, str) and ':' in port:
                host_port, container_port = port.split(':')
                # Remove protocol if present
                container_port = container_port.split('/')[0]
                port_dict[f"{container_port}/tcp"] = int(host_port)
        return port_dict

    def _parse_volumes(self, volumes: list) -> Dict:
        """Parse volume mappings from docker-compose format"""
        volume_dict = {}
        for volume in volumes:
            if isinstance(volume, str) and ':' in volume:
                host_path, container_path = volume.split(':')[:2]
                
                # Convert to absolute path if relative
                if not os.path.isabs(host_path):
                    host_path = os.path.abspath(host_path)
                
                # Ensure host path exists
                os.makedirs(host_path, exist_ok=True)
                
                volume_dict[host_path] = {'bind': container_path, 'mode': 'rw'}
        return volume_dict
    
    def stop_container(self, instance_id: str) -> Tuple[bool, str]:
        """Stop a running container"""
        try:
            container = self.client.containers.get(instance_id)
            container.stop(timeout=20)
            return True, f"Container {instance_id} stopped"
        except docker.errors.NotFound: # type: ignore
            return False, f"Container {instance_id} not found"
        except Exception as e:
            return False, f"Error stopping container: {e}"
    
    def start_container(self, instance_id: str) -> Tuple[bool, str]:
        """Start a stopped container"""
        try:
            container = self.client.containers.get(instance_id)
            container.start()
            return True, f"Container {instance_id} started"
        except docker.errors.NotFound: # type: ignore
            return False, f"Container {instance_id} not found"
        except Exception as e:
            return False, f"Error starting container: {e}"
    
    def remove_container(self, instance_id: str, force: bool = False) -> Tuple[bool, str]:
        """Remove a container"""
        try:
            container = self.client.containers.get(instance_id)
            container.remove(force=force)
            return True, f"Container {instance_id} removed"
        except docker.errors.NotFound:  # type: ignore
            return False, f"Container {instance_id} not found"
        except Exception as e:
            return False, f"Error removing container: {e}"
    
    def get_container_status(self, instance_id: str) -> Optional[str]:
        """Get container status"""
        try:
            container = self.client.containers.get(instance_id)
            return container.status
        except docker.errors.NotFound:  # type: ignore
            return None
        except Exception as e:
            print(f"Error getting container status: {e}")
            return None
    
    def get_container_logs(self, instance_id: str, tail: int = 100) -> str:
        """Get container logs"""
        try:
            container = self.client.containers.get(instance_id)
            return container.logs(tail=tail).decode('utf-8')
        except Exception as e:
            return f"Error getting logs: {e}"
