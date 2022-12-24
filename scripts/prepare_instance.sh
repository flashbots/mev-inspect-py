# Update the dependencies.
sudo apt-get update &&

# Install Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common -y &&
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - &&
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable" &&
sudo apt install docker-ce -y &&

# Install minikube
sudo apt install -y curl wget apt-transport-https -y &&
wget https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 &&
sudo cp minikube-linux-amd64 /usr/local/bin/minikube &&
sudo chmod +x /usr/local/bin/minikube &&
minikube version &&

# Install kubectl
sudo curl -fsSLo /etc/apt/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg &&
echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list &&
sudo apt-get update &&
sudo apt-get install -y kubelet kubeadm kubectl &&
sudo apt-mark hold kubelet kubeadm kubectl &&

# Install Kind.
# curl -Lo ./kind "https://kind.sigs.k8s.io/dl/v0.17.0/kind-$(uname)-amd64" &&
# chmod +x ./kind &&
# sudo mv ./kind /usr/local/bin/kind &&

# Install pip
sudo apt install python3-pip -y &&

# Install postgres lib
sudo apt-get install -y libpq-dev &&

# Install go
rm -rf /usr/local/go ; wget https://go.dev/dl/go1.19.4.linux-amd64.tar.gz && tar -C /usr/local -xzf go1.19.4.linux-amd64.tar.gz &&
export PATH=$PATH:/usr/local/go/bin &&

# Install tilt
curl -fsSL https://raw.githubusercontent.com/tilt-dev/tilt/master/scripts/install.sh | bash &&

# Install poetry
curl -sSL https://install.python-poetry.org | python3 - &&
export PATH=$HOME/.local/bin:$PATH &&

# Clone the repository and prepare the enviro nment
git clone https://github.com/IlluvatarEru/mev-inspect-py.git &&
cd mev-inspect-py &&
python3 -m pip install cytoolz &&
poetry install

echo -e "\nexport PATH=$HOME/.local/bin:$PATH" >> $HOME/.bashrc &&
echo -e "\nexport PATH=$PATH:/usr/local/go/bin" >> $HOME/.bashrc &&

echo -e "\nAt this point, think about running the reset command before using mev-inspect-py\n"
